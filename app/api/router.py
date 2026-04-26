from typing import Any

from fastapi import APIRouter

from app.api.schemas.shipment import (
    CreateShipment,
    ReadShipment,
    UpdateShipment,
)
from app.database.session import SessionDep
from app.services.shipment import ShipmentService

router = APIRouter()

@router.get("/shipment/{id}", response_model=ReadShipment)
async def get_shipment_by_id(id : int, session : SessionDep) :
    return await ShipmentService(session).get(id)

@router.post("/shipment", response_model= ReadShipment)
async def create_shipment(data : CreateShipment, session : SessionDep):
    return await ShipmentService(session).create(data)

@router.patch("/shipment/{id}", response_model=ReadShipment)
async def patch_update_shipment(id : int, data: UpdateShipment, session: SessionDep):
    return await ShipmentService(session).update(id, data)

@router.delete("/shipment/{id}")
async def delete_shipment(id : int, session: SessionDep) -> dict[str, Any]:
    await ShipmentService(session).delete(id)
    return {"message": f"Shipment with id {id} deleted successfully"}