import resend
from fastapi import BackgroundTasks
from fastapi_mail import MessageSchema, MessageType
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import EmailStr
from twilio.http.async_http_client import AsyncTwilioHttpClient
from twilio.rest import Client

from app.config import notification_settings, twilio_settings
from app.utils import TEMPLATE_DIR

resend.api_key = notification_settings.RESEND_API_KEY

__jinja = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR), autoescape=select_autoescape(["html"])
)


def _send_email(receipients: list[str], subject: str, html: str):
    resend.Emails.send(
        {
            "from": notification_settings.MAIL_FROM,
            "to": receipients,
            "subject": subject,
            "html": html,
        }
    )


class NotificationService:
    def __init__(self, tasks: BackgroundTasks):
        self.tasks = tasks

    async def send_email(self, recipients: list[EmailStr], subject: str, body: str):

        ## tasks takes function name first and then the argument
        self.tasks.add_task(
            self.fastmail.send_message,
            message=MessageSchema(
                recipients=recipients,
                subject=subject,
                body=body,
                subtype=MessageType.plain,
            ),
        )

    async def send_message_with_template(
        self,
        recipients: list[EmailStr],
        subject: str,
        context: dict,
        template_name: str,
    ):
        html = __jinja.get_template(template_name).render(**context)
        self.tasks.add_task(_send_email, recipients, subject, html)

    async def send_sms(self, to: str, body: str):
        async_client = AsyncTwilioHttpClient()
        client = Client(
            twilio_settings.ACCOUNT_SID,
            twilio_settings.AUTH_TOKEN,
            http_client=async_client,
        )
        try:
            message = await client.messages.create_async(
                from_=twilio_settings.PHONE_NUMBER, to=to, body=body
            )
            if message:
                print("Message SID:", message.sid)
                print("Message status:", message.status)
            else:
                print("Message creation returned None")
        except Exception as e:
            print("SMS error:", e)
