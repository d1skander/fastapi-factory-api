from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from sqlalchemy import select

from typing import Annotated

from schemas.user_shemas import Worker as WorkerShemas
from schemas.user_shemas import WorkerAuth as WorkerAuthShemas
from schemas.token_shemas import Token as TokenShemas

from database.models.main_models import Worker as WorkerModel
from database.settings import get_db

from core.user.password_security import password_hash
from core.user.dependence import get_verification_id
from core.token.token_security import create_access_token


import os
import datetime


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
def auth_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
              db: Session = Depends(get_db)) -> TokenShemas:
    verification_id = form_data.username
    stmt = select(WorkerModel).where(WorkerModel.verification_id == verification_id)
    result = db.execute(stmt).scalar_one_or_none()
    if not result == None:
        access_token_expires = datetime.timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
        access_token = create_access_token(
        data={"sub": result.id}, expires_delta=access_token_expires
    )
        return TokenShemas(access_token=access_token, token_type="bearer")
    else:
        raise Exception(f"Не существует такого пользователя: {verification_id}")