
from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.config import notification_settings

from pydantic import EmailStr


class NotificationService:
    def __init__(self, tasks : BackgroundTasks):
        self.tasks = tasks
        self.fastmail = FastMail(
            ConnectionConfig(
                **notification_settings.model_dump()
            )
        )

    async def send_email(self, recipients : list[EmailStr], subject : str, body : str):

        ## tasks takes function name first and then the argument
        self.tasks.add_task(
            self.fastmail.send_message,
            message = MessageSchema(
                recipients=recipients,
                subject=subject,
                body=body,  
                subtype=MessageType.plain
        )
        )