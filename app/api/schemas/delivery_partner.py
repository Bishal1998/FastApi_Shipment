from pydantic import BaseModel, EmailStr
from uuid import UUID

from sqlmodel import Field


class BaseDeliveryPartner(BaseModel):
    name: str
    email: EmailStr
    serviceable_zipcodes: list[int]
    max_handling_capacity: int


class CreateDeliveryPartner(BaseDeliveryPartner):
    password: str


class UpdateDeliveryPartner(BaseModel):
    serviceable_zipcodes: list[int] | None = Field(default=None)
    max_handling_capacity: int | None = Field(default=None)


class ReadDeliveryPartner(BaseDeliveryPartner):
    id: UUID
