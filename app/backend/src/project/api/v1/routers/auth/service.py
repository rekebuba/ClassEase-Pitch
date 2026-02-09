from pathlib import Path
from typing import List

from fastapi import HTTPException, status
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from google.auth.transport import requests
from google.oauth2 import id_token
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from pydantic import BaseModel, EmailStr, NameEmail
from sqlalchemy.orm import Session

from project.core.config import settings
from project.models import AuthIdentity, User
from project.utils.enum import AuthProviderEnum

serializer = URLSafeTimedSerializer(settings.SECRET_KEY.get_secret_value())


class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
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
    TEMPLATE_FOLDER=Path(__file__).parent.parent.parent.parent.parent / "templates",
)


def generate_email_verification_token(email: EmailStr) -> str:
    return serializer.dumps(email, salt="email-verification")


def verify_email_verification_token(token: str, max_age: int = 60 * 60 * 24):
    try:
        email = serializer.loads(
            token,
            salt="email-verification",
            max_age=max_age,  # 24 hours
        )
        return email
    except SignatureExpired:
        return None
    except BadSignature:
        return None


async def send_verification_email(email_to: NameEmail):
    token = generate_email_verification_token(email_to.email)
    verification_link = f"{settings.FRONTEND_HOST}/verify-email?token={token}"

    message = MessageSchema(
        subject="Verify your email",
        recipients=[email_to],
        template_body={
            "verification_link": verification_link,
            "app_name": "ClassEase",
            "user_name": email_to.name,
            "expires_in": 24,
            "year": 2026,
        },
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name="email/verification.html")


def verify_google_token(token: str) -> dict:
    try:
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), settings.GOOGLE_CLIENT_ID
        )
        return idinfo
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Google token"
        )


def get_google_user(db: Session, token: str) -> User:
    """Retrieve or link a user based on Google token data."""

    google_data = verify_google_token(token)

    if not google_data.get("email_verified", False):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Google account email is not verified",
        )

    google_sub = google_data["sub"]
    email = google_data["email"]

    # Try to find a user linked by Google
    linked_identity = (
        db.query(AuthIdentity)
        .filter(
            AuthIdentity.provider == AuthProviderEnum.GOOGLE,
            AuthIdentity.provider_user_id == google_sub,
        )
        .first()
    )

    if linked_identity:
        return linked_identity.user

    # Try to find user by email (existing known user)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # Check if Google identity already exists for this user (safety)
    existing_identity = (
        db.query(AuthIdentity)
        .filter(
            AuthIdentity.user_id == user.id,
            AuthIdentity.provider == AuthProviderEnum.GOOGLE,
        )
        .first()
    )
    if not existing_identity:
        # Create new Google identity linked to the user
        identity = AuthIdentity(
            user_id=user.id,
            provider=AuthProviderEnum.GOOGLE,
            provider_user_id=google_sub,
        )
        user.is_verified = True  # Mark user as verified since Google email is verified
        db.add(identity)
        db.commit()

    return user
