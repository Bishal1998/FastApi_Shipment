from typing import Annotated
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr

from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import (
    CurrentDeliveryPartnerDep,
    get_delivery_partner_access_token,
    DeliveryPartnerServiceDep,
)
from app.api.schemas.delivery_partner import (
    CreateDeliveryPartner,
    ReadDeliveryPartner,
    UpdateDeliveryPartner,
)
from app.database.redis import add_jti_to_blacklist

from fastapi import Request

from app.config import app_settings

from app.utils import TEMPLATE_DIR

router = APIRouter(
    prefix="/partner",
    tags=["Delivery Partner"],
)


@router.post("/signup", response_model=ReadDeliveryPartner)
async def signup(data: CreateDeliveryPartner, service: DeliveryPartnerServiceDep):
    return await service.add(data)


@router.post("/login")
async def login(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: DeliveryPartnerServiceDep,
):
    token = await service.login(request_form.username, request_form.password)
    return {"access_token": token, "type": "jwt"}


@router.put("/update")
async def update_delivery_partner(
    data: UpdateDeliveryPartner,
    partner: CurrentDeliveryPartnerDep,
    service: DeliveryPartnerServiceDep,
):
    return await service.update(partner.id, data)


@router.get("/logout")
async def logout(
    token_data: Annotated[dict, Depends(get_delivery_partner_access_token)],
):
    await add_jti_to_blacklist(token_data["jti"])
    return {"detail": "Logged out successfully"}


@router.get("/verify")
async def verify_seller_email(token : str, service : DeliveryPartnerServiceDep):
    await service.verify_email(token)
    return {
        "detail" : "Account is verified"
    }


@router.get("/forgot-password")
async def forgot_password(email : EmailStr, service : DeliveryPartnerServiceDep):
    await service.forgot_password(email, router_prefix="seller")
    return {
        "detail" : "Check email for password reset link"
    }

@router.get("/password-reset")
async def password_reset(token : str, password : Annotated[str, Form()],  service : DeliveryPartnerServiceDep):
    await service.reset_password(token, password)
    return {
        "detail" : "Password reset successfully"
    }


@router.get("/reset-password-form")
async def get_password_reset_form(request : Request, token : str):
    templates = Jinja2Templates(TEMPLATE_DIR)

    return templates.TemplateResponse(
        request=request,
        name="password_reset_form.html",
        context={
            "reset_url":f"http://{app_settings.APP_DOMAIN}/partner/password-reset?token={token}"
        }
    )