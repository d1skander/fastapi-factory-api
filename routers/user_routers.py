from fastapi import APIRouter

from shemas.user_shemas import Worker as WorkerShemas


router = APIRouter(prefix="/users", tags=["Пользователи(Дополнительные роутеры)"])


@router.post("/registration")
def registration_user(shema: WorkerShemas):
    return True


@router.post("/auth")
def auth_user():
    pass