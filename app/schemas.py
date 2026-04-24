from pydantic import BaseModel, Field
from random import randint
from enum import Enum
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

class CreateShipment(BaseShipment):
    pass

class UpdateShipment(BaseModel):
    content : str | None = None
    weight : float | None = None
    destination :int | None  = None
    status : ShipmentStatus