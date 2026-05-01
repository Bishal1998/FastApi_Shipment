
import asyncio

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from app.config import notification_settings

fastmail = FastMail(
    ConnectionConfig(
        **notification_settings.model_dump()
    )
)

async def send_message():
    await fastmail.send_message(
        message=MessageSchema(
            recipients=["pandit.15@wright.edu", "paudel.31@wright.edu"],
            subject="Welcome to FastShip",
            body="Things are about to get Interesting!!",
            subtype=MessageType.plain
        )
    )
    print("Email sent!")

asyncio.run(send_message())