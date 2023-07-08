from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

class Jobs(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    recipe_name = Column(String)
    recipe = Column(String)
    ingredients = Column(String)
    image = Column(String)
    status = Column(String)
