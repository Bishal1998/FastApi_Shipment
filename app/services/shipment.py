
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.shipment import CreateShipment, UpdateShipment
from app.database.models import Shipment, ShipmentStatus


class ShipmentService:  

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id : int) -> Shipment:
        shipment = await self.session.get(Shipment, id)

        if not shipment:
            raise HTTPException(status_code=404, detail=f"Shipment with id {id} not found")
        
        return shipment


    async def create(self, data: CreateShipment) -> Shipment:
        
        new_shipment = Shipment(
            **data.model_dump(),
            status = ShipmentStatus.PLACED,
            estimated_delivery = datetime.now() + timedelta(days=7)
        )

        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)
        return new_shipment

    async def update(self, id:int, data: UpdateShipment) -> Shipment:
        
        shipment = await self.get(id)
    
        shipment.sqlmodel_update(data.model_dump(exclude_none=True))

        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)
        return shipment

    async def delete(self, id: int) -> None:
        shipment = await self.get(id)

        await self.session.delete(shipment)
        await self.session.commit()

