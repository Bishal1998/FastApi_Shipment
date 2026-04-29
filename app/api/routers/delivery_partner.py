from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import (
    CurrentDeliveryPartnerDep,
    SellerServiceDep,
    get_delivery_partner_access_token,
)
from app.api.schemas.delivery_partner import (
    CreateDeliveryPartner,
    ReadDeliveryPartner,
    UpdateDeliveryPartner,
)
from app.database.redis import add_jti_to_blacklist

router = APIRouter(
    prefix="/partner",
    tags=["Delivery Partner"],
)


@router.post("/signup", response_model=ReadDeliveryPartner)
async def signup(data: CreateDeliveryPartner, service):
    return await service.add(data)


@router.post("/login")
async def login(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: SellerServiceDep,
):
    token = await service.login(request_form.username, request_form.password)
    return {"access_token": token, "type": "jwt"}


@router.put("/update")
async def update_delivery_partner(
    data: UpdateDeliveryPartner, partner: CurrentDeliveryPartnerDep, service
):
    return await service.update_delivery_partner(partner.id, data)


@router.get("/logout")
async def logout(
    token_data: Annotated[dict, Depends(get_delivery_partner_access_token)],
):
    await add_jti_to_blacklist(token_data["jti"])
    return {"detail": "Logged out successfully"}
