from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from schemas.user_shemas import Worker as WorkerShemas

from database.models.main_models import Worker as WorkerModel
from database.settings import get_db

from core.password_security import password_hash


router = APIRouter(prefix="/workers", tags=["Пользователи(Дополнительные роутеры)"])


@router.post("/worker")
def registration_user(shema: WorkerShemas,
                      db: Session = Depends(get_db)):
    data = shema.model_dump()
    get_password = data.get("password")
    data["password"] = password_hash(str(get_password))
    new_worker = WorkerModel(**data)
    db.add(new_worker)
    db.commit()


@router.post("/auth")
def auth_user():
    pass