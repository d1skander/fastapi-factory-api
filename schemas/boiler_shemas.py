from pydantic import BaseModel

from .main_shemas import BoilerWorkState


import uuid


class Boiler(BaseModel):
    id: uuid.UUID
    name: str
    power: int
    work_state: BoilerWorkState
    #order_id: uuid.UUID
    #worker: str