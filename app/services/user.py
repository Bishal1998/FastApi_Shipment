from app.database.models import User
from app.services.notification_service import NotificationService
from app.services.base import BaseService

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from fastapi import BackgroundTasks, HTTPException, status
import bcrypt
from app.utils import generate_access_token, generate_url_safe_token

from app.config import app_settings


class UserService(BaseService):
    def __init__(self, model: User, session: AsyncSession, tasks : BackgroundTasks):
        super().__init__(model, session)
        self.notification_service = NotificationService(tasks)

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

        user = await self._add(user)

        verify_email_token = generate_url_safe_token({
            "email" : user.email,
            "id" : user.id
        })

        self.notification_service.send_message_with_template(
            recipients = [user.email],
            subject = "Verify your email",
            context = {
                "username" : user.name,
                "verification_url" : f"http://{app_settings.APP_DOMAIN}/user/verify?token={verify_email_token}"
            },
            template_name = "mail_email_verify.html"
        )

        return user

    async def _generate_token(self, email, password) -> str:

        user = await self._get_by_email(email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with email: {email} not found",
            )

        password_matched = bcrypt.checkpw(
            password.encode("utf-8"), user.hashed_password.encode("utf-8")
        )

        if not password_matched:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
            )
        
        if not user.email_verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not verified"
            )

        token = generate_access_token(
            data={
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                }
            }
        )

        return token
