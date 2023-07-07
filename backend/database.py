from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import sqlite3

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

class Jobs(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    recipe_name = Column(String)
    recipe = Column(String)
    ingredients = Column(String)
    image = Column(String)


def initialize_db():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    create_table_query = """
        CREATE TABLE IF NOT EXISTS jobs (
            id STRING PRIMARY KEY,
            recipeName TEXT,
            recipe TEXT,
            ingredients TEXT,
            image TEXT,
            status TEXT
        );"""
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    connection.close()
