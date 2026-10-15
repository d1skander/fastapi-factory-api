from dotenv import load_dotenv

from typing import Annotated

from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session
from sqlalchemy import select

from schemas.token_shemas import TokenData

from database.settings import get_db
from database.models.main_models import Worker as WorkerModel

from .token_security import oauth2_sheme


import jwt
import os


load_dotenv()


async def get_current_user(token: Annotated[str, Depends(oauth2_sheme)], session: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Не удалось проверить учетные данные",
                                          headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=os.getenv("ALGORITHM"))
        id = payload.get("sub")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except jwt.InvalidTokenError:
        raise credentials_exception
    stmt = select(WorkerModel).where(WorkerModel.id == token_data.id)
    result = session.execute(stmt).scalar_one_or_none()
    if result is None:
        raise credentials_exception
    return result.id


async def get_current_active_user(current: Annotated[WorkerModel, Depends(get_current_user)]):
    if not current:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неактивный пользователь")
    return current