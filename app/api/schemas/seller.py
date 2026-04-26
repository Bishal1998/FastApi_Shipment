from pydantic import BaseModel, EmailStr


class BaseSeller(BaseModel):
    name:str
    email:EmailStr

class CreateSeller(BaseSeller):
    password : str

class ReadSeller(BaseSeller):
    id : int