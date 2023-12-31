import json

from fastapi import FastAPI, File, UploadFile
from Lunchpad.src.inv_cook import custom_inference
from pydantic import BaseModel

app = FastAPI()


@app.post("/v1/generateImage")
async def generateImage(image: UploadFile = File(...)):
    image = await image.read()  # FIXME: Download image from request and download.
    recipe_name, recipe, ingredients, new_image = await custom_inference(image)
    return json.dumps({"Image": "fake recipe"})
