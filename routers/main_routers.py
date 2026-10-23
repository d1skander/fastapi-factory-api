from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session

from schemas.main_shemas import Order as OrderShema
from schemas.main_shemas import BoilerStatus

from database.models.main_models import Order as OrderModel
from database.models.main_models import Boiler as BoilerModel
from database.models.main_models import Worker as WorkerModel

from database.settings import get_db

from core.token.dependence import get_current_active_user

from typing import Annotated, List


import uuid
import json


router = APIRouter(prefix='/orders', tags=["Заказы(Основные роутеры)"])


@router.post("/orders")
def manager_order(current: Annotated[str, Depends(get_current_active_user)],
                  response: Response,
                  shema: OrderShema,
                  db: Session = Depends(get_db)):
    correct_grades = ["Director", "Foreman", "Shop_chief", "Chief_eng"]
    stmt = select(WorkerModel).where(WorkerModel.id == current)
    worker = db.execute(stmt).scalar_one_or_none()
    if worker is None:
        response.status_code = 404
        return {"status": response}
    if worker.grades in correct_grades:
        order = OrderModel(id=None, 
                           text_order=shema.text_order,
                           status=shema.status)
        db.add(order)
        db.commit()
        response.status_code = 201
        return {"status": response}
    else:
        response.status_code = 403
        return {"status": response}


@router.get("/orders", response_model=List[OrderShema])
def get_all_info_order(db: Session = Depends(get_db)):
    order = db.execute(select(OrderModel)).scalars().all()
    result = [ord for ord in order]
    data = {}
    for res in result:
        data = {"id": res.id,
                "boiler": res.boiler,
                "text_order": res.text_order,
                "status": res.status}
    if order is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_302_FOUND)


@router.get("/orders/{order_id}", response_model=List[OrderShema])
def get_info_order(order_id: uuid.UUID,
                   db: Session = Depends(get_db)):
    stmt = select(OrderModel).where(OrderModel.id == order_id)
    order = db.execute(stmt).scalar_one_or_none()
    if order is None:
        return Response(status_code=404)
    else:
        data = {"id": order.id,
                "boiler": order.boiler,
                "text_order": order.text_order,
                "status": order.status}
        return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_302_FOUND)


@router.patch("orders/{order_id}/{status_order}")
def get_order_status(current: Annotated[str, Depends(get_current_active_user)],
                     order_id: uuid.UUID,
                     status_order: BoilerStatus,
                     db: Session = Depends(get_db)):
    sender = db.execute(select(WorkerModel).where(WorkerModel.id == current)).scalar_one_or_none()
    if sender is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                            detail={"message": "Пользователь не найден."})
    else:
        if sender.grades in ["Rank_5_6", "Eng_cat_2", "Eng_cat_1", "Chief_spec", "Foreman", "Shop_chief", "Chief_eng", "Director"]:
            order = update(OrderModel).where(OrderModel.id == order_id).values(status = status_order)
            db.execute(order)
            db.commit()
            return Response(status_code=status.HTTP_202_ACCEPTED)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail={"message": "Недоступно."})


@router.delete("orders/{order_id}")
def delete_order(current: Annotated[str, Depends(get_current_active_user)],
                     order_id: uuid.UUID,
                     db: Session = Depends(get_db)):
    sender = db.execute(select(WorkerModel).where(WorkerModel.id == current)).scalar_one_or_none()
    if sender is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                            detail={"message": "Пользователь не найден."})
    else:
        if sender.grades in ["Chief_spec", "Foreman", "Shop_chief", "Chief_eng", "Director"]:
            db.execute(delete(OrderModel).where(OrderModel.id == order_id))
            db.commit()
            return Response(status_code=status.HTTP_202_ACCEPTED)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail={"message": "Недоступно."})