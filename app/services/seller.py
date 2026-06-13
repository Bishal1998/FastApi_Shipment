from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.seller import CreateSeller
from app.database.models import Seller
from app.services.notification_service import NotificationService
from app.services.user import UserService


class SellerService(UserService):
    def __init__(self, session: AsyncSession, notification: NotificationService):
        super().__init__(Seller, session, notification)

    async def add(self, data: CreateSeller) -> Seller:

        return await self._add_user(data.model_dump(), "seller")

    async def login(self, email: str, password: str) -> str:

        return await self._generate_token(email, password)
