import hashlib
import io
import json
import os
import pickle
import sqlite3
from argparse import Namespace
from uuid import uuid4

import ray
import requests
import torch
from database import SessionLocal, engine, get_db
from diffusers import StableDiffusionImg2ImgPipeline
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, UploadFile
from Lunchpad.data import DATA_DIR
from Lunchpad.src.inv_cook import bound_lunchpad_model
from models import Base, Jobs
from PIL import Image
from ray import serve
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import asyncio

app = FastAPI()

Base.metadata.create_all(bind=engine)


@ray.remote 
def custom_inference_wrapper(lunchpad_model, image, id):
    asyncio.run(custom_inference(lunchpad_model, image, id))

async def custom_inference(lunchpad_model, image, id):
    ref = await lunchpad_model.custom_inference.remote(image)
    recipe_name, recipe, ingredients, new_image = await ref

    # This might be a problem creating a new session? Maybe not? Could also pass in the other db session but that's kinda scuffed
    with SessionLocal() as db:
        job = db.query(Jobs).filter(Jobs.id == id).first()
        job.recipe_name = recipe_name
        job.recipe = json.dumps(recipe)
        job.ingredients = json.dumps(ingredients)
        job.image = json.dumps(new_image)
        job.status = "finished"
        db.commit()



@serve.deployment(route_prefix="/v1")
@serve.ingress(app)
class LunchpadAPI:
    def __init__(self, lunchpad_model):
        self.lunchpad_model = lunchpad_model

    # Change this so this is actually polling. Submit 202, then poll on frontend from another endpoint. Return job_id here.
    @app.post("/generate-image", status_code=202)
    async def generate_image(self, image: UploadFile, db: Session = Depends(get_db)):
        image = await image.read()  # FIXME: Download image from request and download
        image = Image.open(io.BytesIO(image)).convert("RGB")

        id = str(uuid4())
        custom_inference_wrapper.remote(self.lunchpad_model, image, id)

        new_job = Jobs(id=id, status="pending")
        db.add(new_job)
        db.commit()
        db.refresh(new_job)

        #Test out why this isn't returning response.

        return {"job_id": id}

    @app.get("/jobs/{job_id}", status_code=200)
    async def get_job(self, job_id: str, db: Session = Depends(get_db)):
        # FIXME: Figure out how to poll here.
        # Figure out why this endpoint isn't getting called.

        job = db.query(Jobs).filter(Jobs.id == job_id).first()
        if job and job.status == "finished":
            return {
                "status": "finished",
                "recipeName": job.recipe_name,
                "recipe": job.recipe,
                "ingredients": job.ingredients,
                "image": job.image,
            }
        else:
            return {"status": "pending"}


deployment = LunchpadAPI.bind(bound_lunchpad_model)


if __name__ == "__main__":
    serve.run(deployment, port=4000)
    resp = requests.post("http://localhost:4000/v1/generate_image")
