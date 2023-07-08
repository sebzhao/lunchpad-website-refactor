import json
import io
import hashlib
import sqlite3
from sqlalchemy.sql import text

from uuid import uuid4
from fastapi import Depends, FastAPI, File, UploadFile, BackgroundTasks
from pydantic import BaseModel
import torch
from Lunchpad.data import DATA_DIR
import ray
from ray import serve
from PIL import Image
import os
import pickle
from argparse import Namespace
from Lunchpad.src.inv_cook import bound_lunchpad_model
from diffusers import StableDiffusionImg2ImgPipeline
from database import engine, Base, SessionLocal, get_db
from models import Jobs


app = FastAPI()


@serve.deployment(route_prefix='/v1')
@serve.ingress(app)
class LunchpadAPI:
    def __init__(self, lunchpad_model):
        self.lunchpad_model = lunchpad_model
        

    # Change this so this is actually polling. Submit 202, then poll on frontend from another endpoint. Return job_id here. 
    @app.post("/generate_image", status_code=202)
    async def generate_image(self, image: UploadFile, background_tasks: BackgroundTasks):
        image = await image.read()  # FIXME: Download image from request and download
        image = Image.open(io.BytesIO(image)).convert("RGB") 

        id = uuid4()
        background_tasks.add_task(self.custom_inference, lunchpad_model = self.lunchpad_model, image=image)

        with get_db() as db:
            new_job = Jobs(id=id, status="pending")
            db.add(new_job)
            db.commit()
            db.refresh(new_job)

        return {"job_id": id}
    
    async def custom_inference(lunchpad_model, image):
        ref = await lunchpad_model.custom_inference.remote(image)
        recipe_name, recipe, ingredients, new_image = await ref


        with get_db() as db:
            job = db.query(Jobs).filter(Jobs.id == id).first()
            job.recipe_name = recipe_name
            job.recipe = json.dumps(recipe)
            job.ingredients = json.dumps(ingredients)
            job.image = json.dumps(new_image)
            job.status = "finished"
            db.commit()



    @app.get("/jobs/{job_id}", status_code=200)
    async def get_job(self, job_id: str):
        # FIXME: Figure out how to poll here.
        
        with get_db() as db:
            job = db.query(Jobs).filter(Jobs.id == job_id).first()
            if job.status == "finished":
                return {"status": "finished", "recipeName": job.recipe_name, "recipe": job.recipe, "ingredients": job.ingredients, "image": job.image}
            else:
                return {"status": "pending"}
    

deployment = LunchpadAPI.bind(bound_lunchpad_model)
