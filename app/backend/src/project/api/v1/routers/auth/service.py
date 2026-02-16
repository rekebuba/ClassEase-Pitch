from datetime import datetime, timedelta, timezone
from typing import List

import pyotp
from fastapi import HTTPException, status
from fastapi_mail import FastMail, MessageSchema, MessageType
from google.auth.transport import requests
from google.oauth2 import id_token
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from pydantic import BaseModel, EmailStr, NameEmail
from redis.asyncio import Redis
from sqlalchemy.orm import Session

from project.core.config import EmailConf, settings
from project.models import AuthIdentity, User
from project.utils.enum import AuthProviderEnum

serializer = URLSafeTimedSerializer(settings.SECRET_KEY.get_secret_value())


class EmailSchema(BaseModel):
    email: List[EmailStr]


def generate_email_verification_token(email: EmailStr) -> str:
    """Generate a token for email verification that expires after a certain time."""
    return serializer.dumps(email, salt="email-verification")


def verify_email_verification_token(token: str, max_age: int = 60 * 60 * 24):
    """Verify the email verification token and return the email if valid."""
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


async def send_verification_email(email_to: NameEmail) -> None:
    """Send an email verification link to the user's email address."""
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

    fm = FastMail(EmailConf)
    await fm.send_message(message, template_name="email/verification.html")


def verify_google_token(token: str) -> dict:
    """Verify the Google token and return the user info if valid."""
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


async def generate_and_store_otp_secret(email: EmailStr, redis_client: Redis) -> str:
    """
    Generates a secret, saves it to Redis, and returns the 6-digit OTP.
    """
    secret = pyotp.random_base32()

    # Store the secret in Redis with an expiration 10 minutes
    redis_key = f"otp:{email}"
    await redis_client.setex(redis_key, timedelta(minutes=10), secret)

    # Using a 5-minute interval so the code doesn't change every 30 seconds
    totp = pyotp.TOTP(secret, interval=600)
    return totp.now()


async def generate_and_store_password_reset_token(
    email: EmailStr,
    redis_client: Redis,
) -> str:
    """Generates a password reset token, saves it to Redis, and returns the token."""
    reset_token = pyotp.random_base32()

    # Store the reset_token in Redis with an expiration 10 minutes
    redis_key = f"password_reset:{email}"
    await redis_client.setex(redis_key, timedelta(minutes=10), reset_token)

    return reset_token


async def verify_otp_and_generate_token(
    email: EmailStr,
    user_submitted_code: str,
    redis_client: Redis,
) -> str | None:
    """
    Retrieves secret from Redis, verifies the OTP, and deletes if valid.
    generates a token if the OTP is valid.
    """
    redis_key = f"otp:{email}"
    secret = await redis_client.get(redis_key)

    if not secret:
        return None  # OTP expired or never requested

    totp = pyotp.TOTP(secret, interval=600)

    # Check if the code is correct
    if not totp.verify(user_submitted_code):
        return None

    # Valid! Delete the secret so it's a "One-Time" password
    await redis_client.delete(redis_key)

    # generate a token
    token = await generate_and_store_password_reset_token(email, redis_client)

    return token


async def verify_password_reset_token(
    email: EmailStr,
    token: str,
    redis_client: Redis,
) -> bool:
    """Verify the password reset token from Redis."""
    redis_key = f"password_reset:{email}"
    stored_token = await redis_client.get(redis_key)

    if not stored_token:
        return False  # Token expired or never generated

    if stored_token != token:
        return False  # Invalid token

    # Valid token, delete it to prevent reuse
    await redis_client.delete(redis_key)
    return True


async def send_reset_password_email(email_to: NameEmail, redis_client: Redis) -> None:
    """Send a password reset email with a tokenized link."""

    otp = await generate_and_store_otp_secret(email_to.email, redis_client)

    project_name = settings.PROJECT_NAME
    message = MessageSchema(
        subject=f"{project_name} - Password recovery for user {email_to.name}",
        recipients=[email_to],
        template_body={
            "app_name": settings.PROJECT_NAME,
            "username": email_to.name,
            "expires_in": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "otp_code": otp,
            "current_year": datetime.now(timezone.utc).year,
        },
        subtype=MessageType.html,
    )
    fm = FastMail(EmailConf)
    await fm.send_message(message, template_name="email/reset_password.html")
