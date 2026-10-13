from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas.boiler_shemas import Boiler as BoilerShema
from schemas.user_shemas import WorkerAuth as WorkerAuthShemas

from database.settings import get_db
from database.models.main_models import Boiler as BoilerModel

from core.token.dependence import get_current_active_user


import uuid


router = APIRouter(prefix='/boilers', tags=["Котлы"])


@router.get("/boilers", response_model=BoilerShema)
def get_all_boilers(db: Session = Depends(get_db)):
    boilers = db.execute(select(BoilerModel)).all()
    return boilers


@router.get("/boilers/{id_boiler}", response_model=BoilerShema)
def get_boiler(id_boiler: uuid.UUID,
               db: Session = Depends(get_db)):
    stmt = select(BoilerModel).where(BoilerModel.id == id_boiler)
    boiler = db.execute(stmt).scalar_one_or_none
    if boiler is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail={"message": "Не найден."})
    return 


'''@router.post("/boilers")
def create_boiler(response: Response,
                  db: Session = Depends(get_db),
                  current: WorkerAuthShemas = Depends(get_current_active_user),
                  shema: BoilerShema):
    stmt = select(BoilerModel).where(BoilerModel.id == shema.id)'''