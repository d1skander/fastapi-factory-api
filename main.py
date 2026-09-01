from fastapi import FastAPI

from routers.main_routers import router as main_routers

from dotenv import load_dotenv


import uvicorn
import os


load_dotenv()


app = FastAPI()


app.include_router(main_routers)


if __name__ == "__main__":
    uvicorn.run("main:app", port=7979, log_level="info")
    #Чтобы запустить используйте команду "uv run uvicorn main:app --reload"