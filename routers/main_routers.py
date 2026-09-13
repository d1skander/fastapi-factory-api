from fastapi import APIRouter

from schemas.main_shemas import Order as OrderShema


router = APIRouter(prefix='/orders', tags=["Заказы(Основные роутеры)"])


@router.post("/orders")
def manager_order(shema: OrderShema):
    return shema


@router.get("/{order_id}")
def get_info_order():
    pass


@router.patch("orders/{order_id}/status")
def get_order_status():
    pass