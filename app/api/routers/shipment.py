from typing import Any

from fastapi import APIRouter

from app.api.dependencies import ServiceDep
from app.api.schemas.shipment import (
    CreateShipment,
    ReadShipment,
    UpdateShipment,
)

router = APIRouter(
    prefix="/shipment",
    tags=["Shipment"],
)


@router.get("/shipment/{id}", response_model=ReadShipment)
async def get_shipment_by_id(
    id: int,
    service: ServiceDep,
):
    return await service.get(id)


@router.post(
    "/shipment",
    response_model=ReadShipment,
)
async def create_shipment(data: CreateShipment, service: ServiceDep):
    return await service.create(data)


@router.patch("/shipment/{id}", response_model=ReadShipment)
async def patch_update_shipment(id: int, data: UpdateShipment, service: ServiceDep):
    return await service.update(id, data)


@router.delete("/shipment/{id}")
async def delete_shipment(id: int, service: ServiceDep) -> dict[str, Any]:
    await service.delete(id)
    return {"message": f"Shipment with id {id} deleted successfully"}
