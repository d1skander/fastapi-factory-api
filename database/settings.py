from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

from database.models.main_models import Base

from typing import Annotated

from fastapi import Depends


import os


load_dotenv()


SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{os.getenv("USER_DB")}:{os.getenv("PASSWORD_DB")}@{os.getenv("HOST_DB")}:{os.getenv("PORT_DB")}/{os.getenv("NAME_DB")}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    with SessionLocal() as db:
        yield db


def create_db():
    Base.metadata.create_all(bind=engine)