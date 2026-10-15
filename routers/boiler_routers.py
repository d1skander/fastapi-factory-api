from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas.boiler_shemas import Boiler as BoilerShema

from database.settings import get_db
from database.models.main_models import Boiler as BoilerModel
from database.models.main_models import Worker as WorkerModel

from core.token.dependence import get_current_active_user

from typing import Annotated


import uuid


router = APIRouter(prefix='/boilers', tags=["Котлы"])


@router.get("/boilers", response_model=BoilerShema)
def get_all_boilers(responce: Response, 
                    db: Session = Depends(get_db)):
    boilers = db.execute(select(BoilerModel)).all()
    if boilers is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                    detail={"message": "Не найдено."})
    responce.status_code = 304
    return Response(content={boilers}, status_code=responce.status_code)


@router.get("/boilers/{id_boiler}", response_model=BoilerShema)
def get_boiler(responce: Response,
               id_boiler: uuid.UUID,
               db: Session = Depends(get_db),):
    stmt = select(BoilerModel).where(BoilerModel.id == id_boiler)
    boiler = db.execute(stmt).scalar_one_or_none()
    if boiler is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail={"message": "Не найдено."})
    responce.status_code = 304
    return Response(content={boiler}, status_code=responce.status_code)

#Не закончена
@router.post("/boilers")
def create_boiler(current: Annotated[str, Depends(get_current_active_user)],
                  shema: BoilerShema,
                  response: Response,
                  db: Session = Depends(get_db)):
    correct_grades = ["Director", "Foreman", "Shop_chief", "Chief_eng"]
    stmt_worker = select(WorkerModel).where(WorkerModel.id == current)
    worker = db.execute(stmt_worker).scalar_one_or_none()
    if worker is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                    detail={"message": "Не найдено."})
    if worker.grades in correct_grades:
        stmt_boiler = BoilerModel()