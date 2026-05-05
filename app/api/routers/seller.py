from typing import Annotated
from pydantic import EmailStr
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import SellerServiceDep, get_seller_access_token
from app.api.schemas.seller import CreateSeller, ReadSeller
from app.database.redis import add_jti_to_blacklist

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


@router.get("/logout")
async def logout(token_data: Annotated[dict, Depends(get_seller_access_token)]):
    await add_jti_to_blacklist(token_data["jti"])
    return {"detail": "Logged out successfully"}


@router.get("/verify")
async def verify_seller_email(token : str, service : SellerServiceDep):
    await service.verify_email(token)
    return {
        "detail" : "Account is verified"
    }

@router.get("/forgot-password")
async def forgot_password(email : EmailStr, service : SellerServiceDep):
    await service.forgot_password(email, router_prefix="seller")
    return {
        "detail" : "Check email for password reset link"
    }

@router.get("/password-reset")
async def password_reset(token : str, password : str,  service : SellerServiceDep):
    await service.reset_password(token, password)
    return {
        "detail" : "Password reset successfully"
    }