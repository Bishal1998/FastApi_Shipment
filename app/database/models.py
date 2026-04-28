from datetime import datetime
from enum import Enum

from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship


class ShipmentStatus(str, Enum):
    PLACED = "Placed"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    OUT_FOR_DELIVERY = "Out for Delivery"


class Shipment(SQLModel, table=True):
    __tablename__ = "shipments"

    id: int = Field(default=None, primary_key=True)
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus = ShipmentStatus.PLACED
    estimated_delivery: datetime

    seller_id: int = Field(foreign_key="sellers.id")
    seller: "Seller" = Relationship(
        back_populates="shipments", sa_relationship_kwargs={"lazy": "selectin"}
    )


class Seller(SQLModel, table=True):
    __name__ = "sellers"

    id: int = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    hashed_password: str

    shipments: list[Shipment] = Relationship(
        back_populates="seller", sa_relationship_kwargs={"lazy": "selectin"}
    )
