from pydantic import BaseModel, Field
from random import randint
from enum import Enum


def random_destination():
    return randint(11000, 11999)

class ShipmentStatus(str, Enum):
    PLACED = "Placed"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    OUT_FOR_DELIVERY = "Out for Delivery"

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