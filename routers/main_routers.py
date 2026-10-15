from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas.main_shemas import Order as OrderShema
from schemas.user_shemas import WorkerAuth as WorkerAuthShemas

from database.models.main_models import Order as OrderModel
from database.models.main_models import Boiler as BoilerModel
from database.models.main_models import Worker as WorkerModel

from database.settings import get_db

from core.token.dependence import get_current_active_user

from typing import Annotated


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


@router.get("/orders")
def get_all_info_order(db: Session = Depends(get_db)):
    stmt = select(OrderModel)
    order = db.execute(stmt).all()
    result = [tuple(ord) for ord in order]
    json_result = json.dumps(result, default=str)
    if order is None:
        return Response(status_code=404)
    else:
        return JSONResponse(content=json_result, status_code=302)

#данная функция еще в доработке
@router.get("/orders/{order_id}")
def get_info_order(order_id: uuid.UUID,
                   db: Session = Depends(get_db)):
    stmt = select(OrderModel).where(OrderModel.id == order_id)
    order = db.execute(stmt).scalar_one_or_none
    if order is None:
        return Response(status_code=404)
    else:
        return Response(content=order, status_code=302)


@router.patch("orders/{order_id}/status")
def get_order_status():
    pass