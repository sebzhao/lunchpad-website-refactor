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
from database import engine

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
        background_tasks.add_task(self.custom_inference, image)
        query = text("INSERT INTO jobs (id, status) VALUES (:id, 'pending')")
        values = {
            "id": id
        }

        with engine.connect() as conn:
            result = await conn.execute(query, )
        if result:
            return {"job_id": id}
        
    async def custom_inference(self, image):
        ref = await self.lunchpad_model.custom_inference.remote(image)
        recipe_name, recipe, ingredients, new_image = await ref
        query = text("UPDATE jobs SET recipe_name = :recipe_name, recipe = :recipe, ingredients = :ingredients, image = :image, status = 'finished' WHERE id = :id")
        values = {
            "recipe_name": recipe_name,
            "recipe": json.dumps(recipe),
            "ingredients": json.dumps(ingredients),
            "image": json.dumps(new_image),
        }
        result = await database.execute(qu)
        return result


    @app.get("/jobs/{job_id}", status_code=200)
    async def get_job(self, job_id: str):
        # FIXME: Figure out how to poll here.
        query = "SELECT * FROM jobs WHERE id = :id"
        values = {
            "id": job_id
        }
        result = await database.fetch_one(query=query, values=values)
        
        if result.status == "finished":
            return {"status": "finished", "recipeName": result.recipe_name, "recipe": json.load(result.recipe), "ingredients": json.load(result.ingredients), "image": json.load(result.image)}
        else:
            return {"status": "pending"}
    

deployment = LunchpadAPI.bind(bound_lunchpad_model)
