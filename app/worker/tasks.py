from celery import Celery

from app.config import settings, notification_settings, twilio_settings

from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from app.utils import TEMPLATE_DIR

from asgiref.sync import async_to_sync

from twilio.rest import Client

from pydantic import EmailStr

fastmail = FastMail(
            ConnectionConfig(
                **notification_settings.model_dump(),
                TEMPLATE_FOLDER=TEMPLATE_DIR,
            )
        )

send_message = async_to_sync(fastmail.send_message)

app = Celery(
    "api_tasks",
    broker= settings.REDIS_URL(9),
    backend=settings.REDIS_URL(9)
)

client = Client(
            twilio_settings.ACCOUNT_SID,
            twilio_settings.AUTH_TOKEN
        )

@app.task
def send_email(
    receipients: list[str],
    subject : str,
    body : str
):
    send_message(
        MessageSchema(
            recipients=receipients,
            subject=subject,
            body=body,
            subtype=MessageType.plain
        ),
    )
    return "Message sent!"

@app.task
def send_message_with_template( 
    recipients : list[EmailStr], 
    subject : str, context : dict, 
    template_name: str):
        send_message(
            message = MessageSchema(
                recipients=recipients,
                subject=subject,
                template_body=context,
                subtype=MessageType.html
        ),
        template_name = template_name
        )

@app.task
def send_sms(to: str, body: str):
        client.message.create(
               from_ = twilio_settings.PHONE_NUMBER,
               to = to,
               body = body
        )