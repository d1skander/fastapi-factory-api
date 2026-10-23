from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import Response

from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update

from typing import Annotated

from datetime import timedelta

from schemas.user_shemas import Worker as WorkerShemas
from schemas.user_shemas import WorkerAuth as WorkerAuthShemas
from schemas.token_shemas import Token as TokenShemas
from schemas.main_shemas import FactoryRank

from database.models.main_models import Worker as WorkerModel
from database.settings import get_db

from core.user.password_security import password_hash, password_check
from core.user.dependence import get_verification_id
from core.token.token_security import create_access_token
from core.token.dependence import get_current_active_user

from dotenv import load_dotenv


import uuid


load_dotenv()


ACCESS_TOKEN_EXPIRE_MINUTES = 30


router = APIRouter(prefix="/workers", tags=["Рабочие(Дополнительные роутеры)"])


@router.post("/worker")
def registration_user(shema: WorkerShemas,
                      db: Session = Depends(get_db)):
    data = shema.model_dump()
    get_password = data.get("password")
    data["password"] = password_hash(str(get_password))
    new_worker = WorkerModel(**data)
    db.add(new_worker)
    db.commit()


@router.get("/worker", response_model=WorkerAuthShemas)
def get_worker(current: WorkerAuthShemas = Depends(get_current_active_user)):
    return current


@router.patch("/worker/{id}/{new_rank}")
def edit_role_worker(id: uuid.UUID, 
                     new_rank: FactoryRank,
                     db: Session = Depends(get_db),
                     current: WorkerAuthShemas = Depends(get_current_active_user)):
    sender = db.execute(select(WorkerModel).where(WorkerModel.id == current)).scalar_one_or_none()
    if sender is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                                         detail={"message": "Пользователь не найден."})
    else:
        if sender.grades in ["Director", "Foreman", "Shop_chief", "Chief_eng"]:
            new_worker = update(WorkerModel).where(WorkerModel.id == id).values(grades=new_rank)
            db.execute(new_worker)
            db.commit()
            return Response(status_code=status.HTTP_202_ACCEPTED)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                                                     detail={"message": "Роль не подходит."})


@router.post("/auth")
def auth_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
              db: Session = Depends(get_db)):
    verification_id = form_data.username
    stmt = select(WorkerModel).where(WorkerModel.verification_id == verification_id)
    result = db.execute(stmt).scalar_one_or_none()
    if not result is None:
        check = password_check(form_data.password, result.password)
        if check:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
            data={"sub": str(result.id)}, expires_delta=access_token_expires
            )
            return TokenShemas(access_token=access_token, token_type="bearer")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                                 detail={"message": "Пользователь не найден."})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                     detail={"message": "Пользователь не найден."})