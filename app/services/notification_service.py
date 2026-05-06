
from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.config import notification_settings, twilio_settings

from pydantic import EmailStr

from app.utils import TEMPLATE_DIR

from twilio.rest import Client
from twilio.http.async_http_client import AsyncTwilioHttpClient


class NotificationService:
    def __init__(self, tasks : BackgroundTasks):
        self.tasks = tasks
        self.fastmail = FastMail(
            ConnectionConfig(
                **notification_settings.model_dump(),
                TEMPLATE_FOLDER=TEMPLATE_DIR,
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

    async def send_message_with_template(self, 
    recipients : list[EmailStr], subject : str, context : dict, template_name: str):
        self.tasks.add_task(
            self.fastmail.send_message,
            message = MessageSchema(
                recipients=recipients,
                subject=subject,
                template_body=context,
                subtype=MessageType.html
        ),
        template_name = template_name
        )

    async def send_sms(self, to: str, body: str):
        async_client = AsyncTwilioHttpClient()
        client = Client(
            twilio_settings.ACCOUNT_SID,
            twilio_settings.AUTH_TOKEN,
            http_client=async_client
        )
        try:
            message = await client.messages.create_async(
                from_=twilio_settings.PHONE_NUMBER,
                to=to,
                body=body
            )
            if message:
                print("Message SID:", message.sid)
                print("Message status:", message.status)
            else:
                print("Message creation returned None")
        except Exception as e:
            print("SMS error:", e)