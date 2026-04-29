from app.database.models import User
from app.services.base import BaseService

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from fastapi import HTTPException, status
import bcrypt
from app.utils import generate_access_token


class UserService(BaseService):
    def __init__(self, model: User, session: AsyncSession):
        super().__init__(model, session)

    async def _get_by_email(self, email: str):
        return await self.session.scalar(
            select(self.model).where(self.model.email == email)
        )

    async def _add_user(self, data: dict):
        user = self.model(
            **data,
            hashed_password=bcrypt.hashpw(
                data["password"].encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8"),
        )

        return await self._add(user)

    async def _generate_token(self, email, password) -> str:

        seller = await self._get_by_email(email)

        if seller is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with email: {email} not found",
            )

        password_matched = bcrypt.checkpw(
            password.encode("utf-8"), seller.hashed_password.encode("utf-8")
        )

        if not password_matched:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
            )

        token = generate_access_token(
            data={
                "user": {
                    "id": str(seller.id),
                    "email": seller.email,
                }
            }
        )

        return token
