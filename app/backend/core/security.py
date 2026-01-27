import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
import jwt
from sqlalchemy.orm import Session

from core.config import settings
from models.blacklist_token import BlacklistToken
from utils.enum import RoleEnum

ALGORITHM = "HS256"


def check_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
    except (ValueError, TypeError):
        # Handle cases where hashed_password is invalid
        return False


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt with auto-generated salt."""
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_bytes.decode("utf-8")


def create_access_token(
    *,
    subject: str,
    role: RoleEnum,
    expires_delta: timedelta | None = None,
) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode: dict[str, Any] = {
        "exp": expire,
        "sub": subject,
        "role": role.value,
        "jti": str(uuid.uuid4()),  # Unique identifier for token
        "iat": datetime.now(timezone.utc),  # Issued at time
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def is_token_blacklisted(token: str, db: Session) -> bool:
    try:
        payload: dict[str, Any] = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM],
            options={
                "verify_exp": False
            },  # We still want to check blacklist even if expired
        )
        jti = payload.get("jti")
        if not isinstance(jti, str):
            return False

        return (
            db.query(BlacklistToken).filter(BlacklistToken.jti == jti).first()
            is not None
        )
    except jwt.PyJWTError:
        return False
