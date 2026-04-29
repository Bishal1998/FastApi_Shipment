from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.shipment import CreateShipment, UpdateShipment
from app.database.models import Seller, Shipment, ShipmentStatus
from app.services.base import BaseService
from app.services.delivery_partner import DeliveryPartnerService


class ShipmentService(BaseService):
    def __init__(self, session: AsyncSession, partner_service: DeliveryPartnerService):
        super().__init__(Shipment, session)
        self.partner_service = partner_service

    async def get(self, id: UUID) -> Shipment:
        shipment = await self._get(id)

        if not shipment:
            raise HTTPException(
                status_code=404, detail=f"Shipment with id {id} not found"
            )

        return shipment

    async def create(self, data: CreateShipment, seller: Seller) -> Shipment:

        new_shipment = Shipment(
            **data.model_dump(),
            status=ShipmentStatus.PLACED,
            estimated_delivery=datetime.now(timezone.utc) + timedelta(days=7),
            seller_id=seller.id,
        )

        partner = await self.partner_service.assign_shipment(new_shipment)

        new_shipment.delivery_partner_id = partner.id

        shipment = await self._add(new_shipment)
        return shipment

    async def update(self, id: UUID, data: UpdateShipment) -> Shipment:

        shipment = await self.get(id)

        # if (
        #     shipment.seller_id != seller.id
        #     or shipment.delivery_partner_id != partner.id
        # ):
        #     raise HTTPException(
        #         status_code=403,
        #         detail="You do not have permission to update this shipment",
        #     )

        shipment.sqlmodel_update(data.model_dump(exclude_none=True))

        return await self._update(shipment)

    async def delete(self, id: UUID, seller: Seller) -> None:
        shipment = await self.get(id)

        if shipment.seller_id != seller.id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to delete this shipment",
            )

        await self._delete(shipment)
