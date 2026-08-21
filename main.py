from fastapi import FastAPI

from dotenv import load_dotenv


import uvicorn
import os


load_dotenv


app = FastAPI()


if __name__ == "__main__":
    uvicorn.run("main:app", port=os.getenv("PORT"), log_level=os.getenv("LOG_INFO"))