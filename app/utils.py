from datetime import datetime, timedelta, timezone

import jwt

from app.config import jwt_settings


def generate_access_token(data: dict, expiry: timedelta = timedelta(hours=1)) -> str:
    return jwt.encode(
        payload={
            **data,
            "exp": datetime.now(timezone.utc) + expiry,
        },
        algorithm=jwt_settings.JWT_ALGORITHM,
        key=jwt_settings.JWT_SECRET_KEY,
    )


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            jwt=token,
            key=jwt_settings.JWT_SECRET_KEY,
            algorithms=[jwt_settings.JWT_ALGORITHM],
        )
    except jwt.PyJWTError:
        return None
