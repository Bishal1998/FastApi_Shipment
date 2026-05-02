from typing import Any
from uuid import UUID

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api.dependencies import CurrentDeliveryPartnerDep, ServiceDep, CurrentSellerDep, DeliveryPartnerServiceDep
from app.api.schemas.shipment import (
    CreateShipment,
    ReadShipment,
    UpdateShipment,
)
from app.database.models import DeliveryPartner
from app.services.shipment import ShipmentService
from app.utils import TEMPLATE_DIR

templates = Jinja2Templates(directory=TEMPLATE_DIR)

router = APIRouter(
    prefix="/shipment",
    tags=["Shipment"],
)


@router.get("/{id}", response_model=ReadShipment)
async def get_shipment_by_id(
    id: UUID,
    service: ServiceDep,
    partner: CurrentDeliveryPartnerDep
):
    return await service.get(id)

@router.get("/tracking/{id}")
async def get_tracking_details(id : UUID, service: ServiceDep, request : Request):
    shipment = await service.get(id)

    context = shipment.model_dump()
    context["status"] = shipment.status
    context["timeline"] = shipment.timeline
    context["partner"] = shipment.delivery_partner.name

    return templates.TemplateResponse(
        request = request,
        name = "track.html",
        context = context
    )

@router.post(
    "/",
    response_model=ReadShipment,
)
async def create_shipment(
    data: CreateShipment, service: ServiceDep, seller: CurrentSellerDep
):
    return await service.create(data, seller)


@router.patch("/{id}", response_model=ReadShipment)
async def patch_update_shipment(
    id: UUID,
    data: UpdateShipment,
    service: ServiceDep,
    partner: CurrentDeliveryPartnerDep,
):
    return await service.update(id, data)


@router.delete("/{id}")
async def delete_shipment(
    id: UUID, service: ServiceDep, seller: CurrentSellerDep
) -> dict[str, Any]:
    await service.delete(id, seller)
    return {"message": f"Shipment with id {id} deleted successfully"}
