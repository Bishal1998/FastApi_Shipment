from datetime import datetime
from random import randint

from pydantic import BaseModel, Field

from .database.models import ShipmentStatus


def random_destination():
    return randint(11000, 11999)

class BaseShipment(BaseModel):
    content : str 
    weight : float
    destination :int | None  = Field(default_factory=random_destination)

class ReadShipment(BaseShipment):
    id : int
    status : ShipmentStatus
    estimated_delivery : datetime

class CreateShipment(BaseShipment):
    pass

class UpdateShipment(BaseModel):
    status : ShipmentStatus | None = Field(default=None)
    estimated_delivery : datetime | None = Field(default=None)