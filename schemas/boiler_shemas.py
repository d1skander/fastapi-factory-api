from pydantic import BaseModel

from .main_shemas import BoilerWorkState


import uuid


class Boiler(BaseModel):
    id: uuid.UUID
    name: str
    work_state: BoilerWorkState
    who_work: str