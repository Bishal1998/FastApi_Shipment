from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import any_, select

from app.api.schemas.delivery_partner import (
    CreateDeliveryPartner,
    UpdateDeliveryPartner,
)
from app.database.models import DeliveryPartner, Shipment
from app.services.user import UserService


class DeliveryPartnerService(UserService):
    def __init__(self, session: AsyncSession):
        super().__init__(DeliveryPartner, session)

    async def add(self, delivery_partner: CreateDeliveryPartner) -> DeliveryPartner:
        return await self._add_user(delivery_partner.model_dump())

    async def update(self, id: UUID, data: UpdateDeliveryPartner) -> DeliveryPartner:
        delivery_partner = await self._get(id)

        if not delivery_partner:
            raise HTTPException(
                status_code=404,
                detail=f"Delivery Partner with id {id} not found",
            )

        delivery_partner.sqlmodel_update(data.model_dump(exclude_none=True))

        return await self._update(delivery_partner)

    async def login(self, email: str, password: str) -> str:
        return await self._generate_token(email, password)

    async def get_partners_by_zipcode(self, zipcode: int):
        return (
            await self.session.scalars(
                select(DeliveryPartner).where(
                    zipcode == any_(DeliveryPartner.serviceable_zipcodes)
                )
            )
        ).all()

    async def assign_shipment(self, shipment: Shipment):
        eligible_partners = await self.get_partners_by_zipcode(shipment.destination)

        for partner in eligible_partners:
            if partner.current_handling_capacity > 0:
                partner.shipments.append(shipment)
                return partner
        raise HTTPException(status_code=406, detail="No delivery partner available")
