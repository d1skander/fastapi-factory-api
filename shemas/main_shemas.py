from pydantic import BaseModel

from enum import Enum


class BoilerStatus(str ,Enum):
    IN_QUEUE = "In_queue"
    ASSEMBLING = "Assembling"
    TESTING = "Testing"
    READY_FOR_SHIPMENT = "Ready_for_shipment"



class Order(BaseModel):
    name: str
    status: BoilerStatus
    power: int