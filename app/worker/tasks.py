import logging

from asgiref.sync import async_to_sync
from celery import Celery
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from twilio.rest import Client

from app.config import notification_settings, settings, twilio_settings
from app.utils import TEMPLATE_DIR

logger = logging.getLogger(__name__)

fastmail = FastMail(
    ConnectionConfig(
        **notification_settings.model_dump(),
        TEMPLATE_FOLDER=TEMPLATE_DIR,
    )
)

send_message = async_to_sync(fastmail.send_message)

app = Celery("api_tasks", broker=settings.REDIS_URL(9), backend=settings.REDIS_URL(9))

client = Client(twilio_settings.ACCOUNT_SID, twilio_settings.AUTH_TOKEN)


@app.task
def send_email(receipients: list[str], subject: str, body: str):
    send_message(
        MessageSchema(
            recipients=receipients,
            subject=subject,
            body=body,
            subtype=MessageType.plain,
        ),
    )
    return "Message sent!"


@app.task
def send_message_with_template(
    recipients: list[EmailStr], subject: str, context: dict, template_name: str
):
    send_message(
        message=MessageSchema(
            recipients=recipients,
            subject=subject,
            template_body=context,
            subtype=MessageType.html,
        ),
        template_name=template_name,
    )


@app.task
def send_sms(to: str, body: str):
    client.message.create(from_=twilio_settings.PHONE_NUMBER, to=to, body=body)


async def send_email_with_template(
    recipients: list[EmailStr], subject: str, context: dict, template_name: str
):
    try:
        await fastmail.send_message(
            message=MessageSchema(
                recipients=recipients,
                subject=subject,
                template_body=context,
                subtype=MessageType.html,
            ),
            template_name=template_name,
        )
        logger.info("EMAIL SENT SUCCESSFULLY")
    except Exception as e:
        logger.error(f"EMAIL ERROR: {type(e).__name__}: {e}")
        raise
