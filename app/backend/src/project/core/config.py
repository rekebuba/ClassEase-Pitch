import os
import warnings
from datetime import date
from functools import lru_cache
from pathlib import Path
from typing import Annotated, Any, Literal, Union

from fastapi_mail import ConnectionConfig
from pydantic import (
    AnyUrl,
    BeforeValidator,
    EmailStr,
    PostgresDsn,
    RedisDsn,
    SecretStr,
    computed_field,
    model_validator,
)
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self

from project.utils.enum import GenderEnum


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


def get_env_file() -> str:
    """Get environment file path."""
    env = os.getenv("ENVIRONMENT", "development")
    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    return os.path.join(repo_root, f".env.{env}")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_ignore_empty=True,
        extra="ignore",
    )

    ENVIRONMENT: Literal["development", "testing", "production"] = "development"
    API_V1_STR: str
    SECRET_KEY: SecretStr
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    FRONTEND_HOST: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    PROJECT_NAME: str

    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: SecretStr
    FIRST_SUPERUSER_NAME: str
    FIRST_SUPERUSER_FATHER_NAME: str
    FIRST_SUPERUSER_GRAND_FATHER_NAME: str
    FIRST_SUPERUSER_DATE_OF_BIRTH: date
    FIRST_SUPERUSER_GENDER: GenderEnum
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PHONE: PhoneNumber
    FIRST_SUPERUSER_ADDRESS: str

    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str

    REDIS_SERVER: str
    REDIS_PORT: int
    REDIS_USER: str
    REDIS_PASSWORD: SecretStr | None = None

    @computed_field
    @property
    def SQLALCHEMY_POSTGRES_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD.get_secret_value(),
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    @computed_field
    @property
    def REDIS_URL(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            password=(
                self.REDIS_PASSWORD.get_secret_value() if self.REDIS_PASSWORD else None
            ),
            host=self.REDIS_SERVER,
            port=self.REDIS_PORT,
        )

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str
    SMTP_USER: str
    SMTP_PASSWORD: SecretStr
    EMAILS_FROM_EMAIL: EmailStr
    EMAILS_FROM_NAME: EmailStr
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self

    @computed_field
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    def _check_default_secret(self, var_name: str, value: SecretStr | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "development":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret(
            "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        )

        return self


class DevSettings(Settings):
    model_config = SettingsConfigDict(env_file=get_env_file())


class TestSettings(Settings):
    model_config = SettingsConfigDict(env_file=get_env_file())


class ProdSettings(Settings):
    model_config = SettingsConfigDict(env_file=get_env_file())

    @computed_field
    @property
    def SQLALCHEMY_POSTGRES_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@/{self.POSTGRES_DB}?host=/cloudsql/{self.POSTGRES_SERVER}"


@lru_cache
def get_settings() -> Union[DevSettings, TestSettings, ProdSettings]:
    # 1. Peek at the environment or a base .env to see what mode we are in
    env_mode = os.getenv("ENVIRONMENT", "development")

    # 2. Map modes to classes
    config_mapping = {
        "production": ProdSettings,
        "testing": TestSettings,
        "development": DevSettings,
    }

    return config_mapping.get(env_mode, DevSettings)()


settings = get_settings()

EmailConf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.EMAILS_FROM_EMAIL,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_FROM_NAME=settings.EMAILS_FROM_NAME,
    MAIL_STARTTLS=settings.SMTP_TLS,
    MAIL_SSL_TLS=settings.SMTP_SSL,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates",
)
