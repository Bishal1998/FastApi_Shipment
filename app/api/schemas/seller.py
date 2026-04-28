from pydantic import BaseModel, EmailStr
from uuid import UUID


class BaseSeller(BaseModel):
    name:str
    email:EmailStr

class CreateSeller(BaseSeller):
    password : str

class ReadSeller(BaseSeller):
    id : UUID