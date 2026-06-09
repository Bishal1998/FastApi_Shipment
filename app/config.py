from pydantic_settings import BaseSettings, SettingsConfigDict

_base_config = SettingsConfigDict(
    env_file="./.env", extra="ignore", env_ignore_empty=True
)


class AppSettings(BaseSettings):
    APP_NAME: str
    APP_DOMAIN: str

    model_config = _base_config


class DatabaseSettings(BaseSettings):
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int

    REDIS_HOST: str
    REDIS_PORT: int

    model_config = _base_config

    @property
    def POSTGRES_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    def REDIS_URL(self, db) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{db}"


class JWTSettings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    model_config = _base_config


class NotificationSettings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    model_config = _base_config


class Twilio_Setting(BaseSettings):
    ACCOUNT_SID: str
    AUTH_TOKEN: str
    PHONE_NUMBER: str

    model_config = _base_config


app_settings = AppSettings()
settings = DatabaseSettings()
jwt_settings = JWTSettings()
notification_settings = NotificationSettings()
twilio_settings = Twilio_Setting()
