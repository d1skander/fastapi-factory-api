from fastapi import APIRouter, Depends

from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas.user_shemas import Worker as WorkerShemas

from database.models.main_models import Worker as WorkerModel
from database.settings import get_db


router = APIRouter(prefix="/workers", tags=["Пользователи(Дополнительные роутеры)"])


@router.post("/worker")
def registration_user(shema: WorkerShemas,
                      db: Session = Depends(get_db)):
    data = shema.model_dump()
    new_worker = WorkerModel(**data)
    db.add(new_worker)
    db.commit()


@router.post("/auth")
def auth_user():
    pass