from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas.main_shemas import Order as OrderShema
from schemas.user_shemas import WorkerAuth as WorkerAuthShemas

from database.models.main_models import Order as OrderModel
from database.models.main_models import Boiler as BoilerModel

from database.settings import get_db

from core.token.dependence import get_current_active_user


import uuid


router = APIRouter(prefix='/orders', tags=["Заказы(Основные роутеры)"])


@router.post("/orders")
def manager_order(response: Response,
                  shema: OrderShema,
                  db: Session = Depends(get_db),
                  current: WorkerAuthShemas = Depends(get_current_active_user),):
    correct_grades = ["Director", "Foreman", "Shop_chief", "Chief_eng"]
    print(correct_grades, current.grades)
    if current.grades in correct_grades:
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
    if order is None:
        return Response(status_code=404)
    else:
        return JSONResponse(content=[x.encode('utf-8') for x in order], status_code=302)


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