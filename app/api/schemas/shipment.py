from datetime import datetime
from random import randint
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr

from app.api.schemas.seller import ReadSeller
from app.database.models import ShipmentEvent, ShipmentStatus


def random_destination():
    return randint(11000, 11999)


class BaseShipment(BaseModel):
    content: str
    weight: float
    destination: int | None = Field(default_factory=random_destination)


class ReadShipment(BaseShipment):
    id: UUID
    timeline : list[ShipmentEvent]
    estimated_delivery: datetime
    seller: ReadSeller


class CreateShipment(BaseShipment):
    client_contact_email:EmailStr | None = Field(default=None)
    client_contact_phone : int | None = Field(default=None)


class UpdateShipment(BaseModel):
    location : int | None = Field(default=None)
    description : str | None = Field(default=None)
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)
