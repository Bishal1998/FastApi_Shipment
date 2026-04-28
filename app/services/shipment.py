from datetime import datetime, timedelta
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.shipment import CreateShipment, UpdateShipment
from app.database.models import Seller, Shipment, ShipmentStatus


class ShipmentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: UUID) -> Shipment:
        shipment = await self.session.get(Shipment, id)

        if not shipment:
            raise HTTPException(
                status_code=404, detail=f"Shipment with id {id} not found"
            )

        return shipment

    async def create(self, data: CreateShipment, seller: Seller) -> Shipment:

        new_shipment = Shipment(
            **data.model_dump(),
            status=ShipmentStatus.PLACED,
            estimated_delivery=datetime.now() + timedelta(days=7),
            seller_id=seller.id,
        )

        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)
        return new_shipment

    async def update(self, id: UUID, data: UpdateShipment, seller: Seller) -> Shipment:

        shipment = await self.get(id)

        if shipment.seller_id != seller.id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to update this shipment",
            )

        shipment.sqlmodel_update(data.model_dump(exclude_none=True))

        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)
        return shipment

    async def delete(self, id: UUID, seller: Seller) -> None:
        shipment = await self.get(id)

        if shipment.seller_id != seller.id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to delete this shipment",
            )

        await self.session.delete(shipment)
        await self.session.commit()
