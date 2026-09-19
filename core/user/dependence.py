from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models.main_models import Worker as WorkerModel
from database.settings import engine


def get_verification_id(get_id: str) -> str:
    stmt = select(WorkerModel).where(WorkerModel.verification_id == get_id)
    with Session(engine) as session:
        data = session.execute(stmt).scalar_one_or_none()
        if data != None:
            return str(data)
        else:
            raise Exception(f"{get_id} не существует")