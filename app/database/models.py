from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import datetime

class ShipmentStatus(str, Enum):
    PLACED = "Placed"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    OUT_FOR_DELIVERY = "Out for Delivery"

class Shipment(SQLModel, table=True):

    __tablename__ = "shipments"

    id : int = Field(default=None, primary_key=True)
    content : str 
    weight : float = Field(le=25)
    destination :int 
    status : ShipmentStatus = ShipmentStatus.PLACED
    estimated_delivery : datetime