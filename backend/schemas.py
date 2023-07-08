from pydantic import BaseModel
from fastapi import UploadFile


class JobCheck(BaseModel):
    job_id: str

class Job(BaseModel):
    id: str
    recipe_name: str
    recipe: str
    ingredients: str
    image: str
    status: str

    class Config:
        orm_mode = True