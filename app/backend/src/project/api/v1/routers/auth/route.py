import logging
from typing import Annotated, Any, Dict

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from project.api.v1.routers.auth.service import (
    get_google_user,
    verify_email_verification_token,
    verify_google_token,
)
from project.api.v1.routers.dependencies import SessionDep, TokenDep, get_db
from project.api.v1.routers.schema import HTTPError
from project.core.config import settings
from project.core.security import ALGORITHM, check_password, create_access_token
from project.models.blacklist_token import BlacklistToken
from project.models.user import User

from .schema import LogOutResponse, Token, VerifyEmailResponse

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    response_model=Token,
    operation_id="login_credential",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": HTTPError,
            "description": "Incorrect Credential",
        },
    },
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user:
        logger.warning(f"Login attempt for non-existent user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not check_password(form_data.password, user.password):
        logger.warning(f"Failed password attempt for user: {user.id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=str(user.id), role=user.role)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/google",
    response_model=Token,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": HTTPError,
            "description": "Invalid Google token or user not found",
        },
    },
)
def google_login(token: str, db: Session = Depends(get_db)):
    google_data = verify_google_token(token)

    user = get_google_user(db, google_data)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    access_token = create_access_token(subject=str(user.id), role=user.role)

    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/verify-email",
    response_model=VerifyEmailResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": HTTPError,
            "description": "Invalid or expired token",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": HTTPError,
            "description": "User not found",
        },
    },
)
def verify_email(
    token: str,
    db: SessionDep,
) -> VerifyEmailResponse:
    email = verify_email_verification_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token",
        )

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.is_verified = True
    db.commit()

    return VerifyEmailResponse(message="Email successfully verified")


@router.post(
    "/logout",
    response_model=LogOutResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": HTTPError,
            "description": "Invalid token format",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": HTTPError,
            "description": "Invalid token",
        },
    },
)
async def logout(
    token: TokenDep,
    db: SessionDep,
) -> Dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[ALGORITHM],
            options={"verify_exp": False},  # Allow logout with expired tokens
        )
        jti = payload.get("jti")

        if not jti:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token format"
            )

        # Check if already blacklisted
        if db.query(BlacklistToken).filter(BlacklistToken.jti == jti).first():
            return {"message": "Token was already invalidated"}

        # Add to blacklist
        blacklisted_token = BlacklistToken(jti=jti)
        db.add(blacklisted_token)
        db.commit()

        return {"message": "Successfully logged out"}

    except jwt.PyJWTError as e:
        logger.error(f"Token validation error during logout: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
