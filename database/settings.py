from sqlalchemy import create_engine

from dotenv import load_dotenv

from database.models.main_models import Base


import os


load_dotenv()


SQLALCHEMY_DATABASE_URL = f"postgresql://{os.getenv("USER_DB")}:{os.getenv("PASSWORD_DB")}@{os.getenv("HOST_DB")}:{os.getenv("PORT_DB")}/{os.getenv("NAME_DB")}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)


def create_db():
    Base.metadata.create_all(bind=engine)