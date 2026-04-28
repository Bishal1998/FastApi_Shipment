from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlalchemy.dialects import postgresql
from sqlmodel import Column, Field, Relationship, SQLModel


class ShipmentStatus(str, Enum):
    PLACED = "Placed"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    OUT_FOR_DELIVERY = "Out for Delivery"


class Shipment(SQLModel, table=True):
    __tablename__ = "shipments"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )
    content: str
    address: int = 2346
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus = ShipmentStatus.PLACED
    estimated_delivery: datetime

    seller_id: UUID = Field(foreign_key="sellers.id")
    seller: "Seller" = Relationship(
        back_populates="shipments", sa_relationship_kwargs={"lazy": "selectin"}
    )


class Seller(SQLModel, table=True):
    __tablename__ = "sellers"

    id: UUID = Field(sa_column=Column(postgresql.UUID, default=uuid4, primary_key=True))
    name: str
    email: EmailStr
    hashed_password: str

    shipments: list[Shipment] = Relationship(
        back_populates="seller", sa_relationship_kwargs={"lazy": "selectin"}
    )
