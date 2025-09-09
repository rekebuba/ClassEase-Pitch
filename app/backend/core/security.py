from datetime import datetime, timedelta
from jose import JWTError  # type: ignore
from passlib.context import CryptContext  # type: ignore
import jwt
import uuid
from core.config import settings
from extension.enums.enum import RoleEnum
from models.blacklist_token import BlacklistToken
from sqlalchemy.orm import Session

pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def check_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    *,
    subject: str,
    role: RoleEnum,
    expires_delta: timedelta | None = None,
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {
        "exp": expire,
        "sub": subject,
        "role": role.value,
        "jti": str(uuid.uuid4()),  # Unique identifier for token  # noqa: F821
        "iat": datetime.utcnow(),  # Issued at time
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def is_token_blacklisted(token: str, db: Session) -> bool:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM],
            options={
                "verify_exp": False
            },  # We still want to check blacklist even if expired
        )
        jti = payload.get("jti")
        if jti is None:
            return False

        return (
            db.query(BlacklistToken).filter(BlacklistToken.jti == jti).first()
            is not None
        )
    except JWTError:
        return False
