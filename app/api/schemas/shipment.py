from datetime import datetime
from random import randint
from uuid import UUID

from pydantic import BaseModel, Field

from app.api.schemas.seller import ReadSeller
from app.database.models import ShipmentStatus


def random_destination():
    return randint(11000, 11999)


class BaseShipment(BaseModel):
    content: str
    weight: float
    destination: int | None = Field(default_factory=random_destination)


class ReadShipment(BaseShipment):
    id: UUID
    status: ShipmentStatus
    estimated_delivery: datetime
    seller: ReadSeller


class CreateShipment(BaseShipment):
    pass


class UpdateShipment(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)
