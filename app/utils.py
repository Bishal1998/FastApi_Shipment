from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

import jwt

from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app.config import jwt_settings

_serializer = URLSafeTimedSerializer(jwt_settings.JWT_SECRET_KEY)

APP_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = APP_DIR/"templates"

def generate_access_token(data: dict, expiry: timedelta = timedelta(hours=1)) -> str:
    return jwt.encode(
        payload={
            **data,
            "jti": str(uuid4()),
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
    
def generate_url_safe_token(data : dict) -> str:
    return _serializer.dumps(data)

def decode_url_safe_token(token : str, expiry : timedelta | None = None) -> dict | None:
    try:
        return _serializer.loads(token, max_age=int(expiry.total_seconds()) if expiry else None)
    except SignatureExpired:
        return None  # token valid but expired
    except BadSignature:
        return None  # token invalid or tampered
    

