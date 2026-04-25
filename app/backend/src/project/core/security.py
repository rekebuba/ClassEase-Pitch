import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable, Optional

import bcrypt
import jwt
from pydantic import SecretStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from project.core.config import settings
from project.models.blacklist_token import BlacklistToken
from project.utils.enum import RoleEnum

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


def get_password_hash(password: SecretStr | str) -> str:
    """Hash a password using bcrypt with auto-generated salt."""
    password_value = (
        password.get_secret_value() if isinstance(password, SecretStr) else password
    )
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_value.encode("utf-8"), salt)
    return hashed_bytes.decode("utf-8")


def create_access_token(
    *,
    subject: str,
    role: RoleEnum,
    school_id: str | None = None,
    school_slug: str | None = None,
    membership_id: str | None = None,
    session_id: str | None = None,
    permissions_version: int | None = None,
    permissions: Optional[Iterable[str]] = None,
    mfa_state: str | None = None,
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
        "school_id": school_id,
        "school_slug": school_slug,
        "membership_id": membership_id,
        "session_id": session_id,
        "permissions_version": permissions_version,
        "permissions": sorted(set(permissions or [])),
        "mfa_state": mfa_state,
        "jti": str(uuid.uuid4()),  # Unique identifier for token
        "iat": datetime.now(timezone.utc),  # Issued at time
    }
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY.get_secret_value(),
        algorithm=ALGORITHM,
    )


async def is_token_blacklisted(token: str, session: AsyncSession) -> bool:
    try:
        payload: dict[str, Any] = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[ALGORITHM],
            options={
                "verify_exp": False
            },  # We still want to check blacklist even if expired
        )
        jti = payload.get("jti")
        if not isinstance(jti, str):
            return False

        return (
            await session.execute(
                select(BlacklistToken).filter(BlacklistToken.jti == jti)
            )
        ).scalar_one_or_none() is not None
    except jwt.PyJWTError:
        return False
