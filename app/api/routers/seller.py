from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import SellerServiceDep
from app.api.schemas.seller import CreateSeller, ReadSeller

from typing import Annotated

router = APIRouter(
    prefix="/seller",
    tags=["Seller"],
)


@router.post("/signup", response_model=ReadSeller)
async def signup(data: CreateSeller, service: SellerServiceDep):
    return await service.add(data)


@router.post("/login")
async def login(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: SellerServiceDep,
):
    token = await service.login(request_form.username, request_form.password)
    return {"access_token": token, "type": "jwt"}
