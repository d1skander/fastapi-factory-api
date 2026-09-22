from fastapi import APIRouter, Depends

from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas.main_shemas import Order as OrderShema
from schemas.user_shemas import WorkerAuth as WorkerAuthShemas

from database.settings import get_db

from core.token.dependence import get_current_active_user


router = APIRouter(prefix='/orders', tags=["Заказы(Основные роутеры)"])


@router.post("/orders")
def manager_order(shema: OrderShema, 
                  db: Session = Depends(get_db),
                  current: WorkerAuthShemas = Depends(get_current_active_user)):
    return shema


@router.get("/{order_id}")
def get_info_order():
    pass


@router.patch("orders/{order_id}/status")
def get_order_status():
    pass