from celery import Celery

from app.config import settings, notification_settings

from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from app.utils import TEMPLATE_DIR

from asgiref.sync import async_to_sync


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