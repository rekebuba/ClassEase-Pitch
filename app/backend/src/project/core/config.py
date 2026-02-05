import os
import secrets
import warnings
from datetime import date
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    EmailStr,
    PostgresDsn,
    computed_field,
    model_validator,
)
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
    repo_root = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
    return os.path.join(repo_root, ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=get_env_file(),
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    FRONTEND_HOST: str = "http://localhost:5173"
    ENVIRONMENT: Literal["development", "testing", "production"] = "development"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    PROJECT_NAME: str

    PROD_POSTGRES_SERVER: str
    PROD_POSTGRES_PORT: int
    PROD_POSTGRES_USER: str
    PROD_POSTGRES_PASSWORD: str
    PROD_POSTGRES_DB: str

    DEV_POSTGRES_SERVER: str
    DEV_POSTGRES_PORT: int
    DEV_POSTGRES_USER: str
    DEV_POSTGRES_PASSWORD: str = ""
    DEV_POSTGRES_DB: str = ""

    TEST_POSTGRES_SERVER: str
    TEST_POSTGRES_PORT: int
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str = ""
    TEST_POSTGRES_DB: str = ""

    @computed_field
    @property
    def SQLALCHEMY_POSTGRES_DATABASE_URI(self) -> PostgresDsn | str:
        if self.ENVIRONMENT == "production":
            # For Cloud SQL Unix Sockets, the format is:
            # postgresql://user:pass@/dbname?host=/cloudsql/connection-name
            return f"postgresql://{self.PROD_POSTGRES_USER}:{self.PROD_POSTGRES_PASSWORD}@/{self.PROD_POSTGRES_DB}?host={self.PROD_POSTGRES_SERVER}"
        elif self.ENVIRONMENT == "development":
            return PostgresDsn.build(
                scheme="postgresql",
                username=self.DEV_POSTGRES_USER,
                password=self.DEV_POSTGRES_PASSWORD,
                host=self.DEV_POSTGRES_SERVER,
                port=self.DEV_POSTGRES_PORT,
                path=self.DEV_POSTGRES_DB,
            )
        elif self.ENVIRONMENT == "testing":
            return PostgresDsn.build(
                scheme="postgresql",
                username=self.TEST_POSTGRES_USER,
                password=self.TEST_POSTGRES_PASSWORD,
                host=self.TEST_POSTGRES_SERVER,
                port=self.TEST_POSTGRES_PORT,
                path=self.TEST_POSTGRES_DB,
            )

    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: EmailStr | None = None
    EMAILS_FROM_NAME: EmailStr | None = None

    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    @computed_field
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    EMAIL_TEST_USER: EmailStr = "test@example.com"
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_SUPERUSER_NAME: str
    FIRST_SUPERUSER_FATHER_NAME: str
    FIRST_SUPERUSER_GRAND_FATHER_NAME: str
    FIRST_SUPERUSER_DATE_OF_BIRTH: date
    FIRST_SUPERUSER_GENDER: GenderEnum
    FIRST_SUPERUSER_EMAIL: str
    FIRST_SUPERUSER_PHONE: str
    FIRST_SUPERUSER_ADDRESS: str

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
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


settings = Settings()  # type: ignore
