
from app.database.models import Shipment, ShipmentEvent, ShipmentStatus
from app.services.base import BaseService


class ShipmentEventService(BaseService):
    def __init__(self, session):
        super().__init__(ShipmentEvent, session)

    async def add(self, shipment:Shipment, location : int | None = None, status : ShipmentStatus | None = None, description : str | None = None):

        if not location or not status:
            last_event = await self.get_latest_event(shipment)

            location = location if location else last_event.location
            status = status if status else last_event.status

        new_event = ShipmentEvent(
            location = location,
            status = status,
            description=description if description else self._generate_description(status, location), 
            shipment_id=shipment.id
        )
        return await self._add(new_event)
    
    async def get_latest_event(self, shipment : Shipment):
       timeline = shipment.timeline
       if not timeline:
        return None
       timeline.sort(key=lambda event: event.created_at)
       return timeline[-1]
    
    def _generate_description(self, status : ShipmentStatus, location : int):
        match status:
            case ShipmentStatus.PLACED:
                return "asssigned delivery partner"
            case ShipmentStatus.OUT_FOR_DELIVERY:
                return "shipment out for delivery"
            case ShipmentStatus.DELIVERED:
                return "successfully delivered"
            case _:
                return f"Scanned at {location}"