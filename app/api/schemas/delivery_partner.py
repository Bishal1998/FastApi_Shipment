from pydantic import BaseModel, EmailStr
from uuid import UUID


class BaseDeliveryPartner(BaseModel):
    name:str
    email:EmailStr
    serviceable_zipcodes: list[int]
    max_handling_capacity: int

class CreateDeliveryPartner(BaseDeliveryPartner):
    password: str

class UpdateDeliveryPartner(BaseModel):
    serviceable_zipcodes: list[int]
    max_handling_capacity: int

class ReadDeliveryPartner(BaseDeliveryPartner):
    id : UUID