from fastapi import FastAPI

from routers.main_routers import router as main_routers
from routers.user_routers import router as user_routers

from dotenv import load_dotenv

from database.settings import create_db, engine

from admin.admin import admin_setup


import uvicorn
import os


load_dotenv()


app = FastAPI()


app.include_router(main_routers)
app.include_router(user_routers)


admin_setup(app, engine)


if __name__ == "__main__":
    create_db()
    uvicorn.run("main:app", port=7979, log_level="info")
    #Чтобы запустить используйте команду "uv run uvicorn main:app --reload"