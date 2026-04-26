from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, HTTPException

from app.api.schemas.shipment import (
    CreateShipment,
    ReadShipment,
    ShipmentStatus,
    UpdateShipment,
)
from app.database.models import Shipment
from app.database.session import SessionDep

router = APIRouter()

@router.get("/shipment/{id}", response_model=ReadShipment)
async def get_shipment_by_id(id : int, session : SessionDep) :
    shipment = await session.get(Shipment, id)

    if not shipment:
        raise HTTPException(status_code=404, detail=f"Shipment with id {id} not found")

    return shipment 

@router.post("/shipment", response_model= ReadShipment)
async def create_shipment(data : CreateShipment, session : SessionDep):

    new_shipment = Shipment(
        **data.model_dump(),
        status = ShipmentStatus.PLACED,
        estimated_delivery = datetime.now() + timedelta(days=7)
    )
    
    session.add(new_shipment)
    await session.commit()
    await session.refresh(new_shipment)

    return new_shipment

@router.patch("/shipment/{id}", response_model=ReadShipment)
async def patch_update_shipment(id : int, data: UpdateShipment, session: SessionDep):

    shipment = await session.get(Shipment, id)

    if not shipment:
        raise HTTPException(status_code=404, detail=f"Shipment with id {id} not found")
    shipment.sqlmodel_update(data.model_dump(exclude_none=True))
    session.add(shipment)
    await session.commit()
    await session.refresh(shipment)
    return shipment 

@router.delete("/shipment/{id}")
async def delete_shipment(id : int, session: SessionDep) -> dict[str, Any]:
    shipment = await session.get(Shipment, id)

    if not shipment:
        raise HTTPException(status_code=404, detail=f"Shipment with id {id} not found")

    await session.delete(shipment)
    await session.commit()

    return {"message": f"Shipment with id {id} deleted successfully"}