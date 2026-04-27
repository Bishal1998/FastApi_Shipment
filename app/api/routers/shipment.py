from typing import Any

from fastapi import APIRouter

from app.api.dependencies import ServiceDep, CurrentSellerDep
from app.api.schemas.shipment import (
    CreateShipment,
    ReadShipment,
    UpdateShipment,
)

router = APIRouter(
    prefix="/shipment",
    tags=["Shipment"],
)


@router.get("/{id}", response_model=ReadShipment)
async def get_shipment_by_id(id: int, service: ServiceDep, seller: CurrentSellerDep):
    return await service.get(id)


@router.post(
    "/",
    response_model=ReadShipment,
)
async def create_shipment(
    data: CreateShipment, service: ServiceDep, seller: CurrentSellerDep
):
    return await service.create(data)


@router.patch("/{id}", response_model=ReadShipment)
async def patch_update_shipment(
    id: int, data: UpdateShipment, service: ServiceDep, seller: CurrentSellerDep
):
    return await service.update(id, data)


@router.delete("/{id}")
async def delete_shipment(
    id: int, service: ServiceDep, seller: CurrentSellerDep
) -> dict[str, Any]:
    await service.delete(id)
    return {"message": f"Shipment with id {id} deleted successfully"}
