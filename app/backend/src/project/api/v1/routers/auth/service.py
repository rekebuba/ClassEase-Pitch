from fastapi import HTTPException, status
from google.auth.transport import requests
from google.oauth2 import id_token
from sqlalchemy.orm import Session

from project.core.config import settings
from project.models import User


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


def get_google_user(db: Session, google_data: dict) -> User | None:
    user = db.query(User).filter(User.google_sub == google_data["sub"]).first()

    return user
