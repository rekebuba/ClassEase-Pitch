import logging
from typing import Annotated, Any, Dict

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr, NameEmail
from sqlalchemy.orm import Session

from project.api.v1.routers.auth.schema import (
    LoginTokenResponse,
    MessageResponse,
    OTPRequest,
    PasswordResetRequest,
    ProviderTokenResponse,
    VerifyOTPResponse,
)
from project.api.v1.routers.auth.service import (
    get_google_user,
    send_reset_password_email,
    verify_email_verification_token,
    verify_otp_and_generate_token,
    verify_password_reset_token,
)
from project.api.v1.routers.dependencies import SessionDep, TokenDep, get_db
from project.api.v1.routers.schema import HTTPError
from project.core.config import settings
from project.core.security import (
    ALGORITHM,
    check_password,
    create_access_token,
    get_password_hash,
)
from project.models import AuthIdentity
from project.models.blacklist_token import BlacklistToken
from project.models.user import User
from project.utils.enum import AuthProviderEnum

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    response_model=LoginTokenResponse,
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
) -> LoginTokenResponse:
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user:
        logger.warning(f"Login attempt for non-existent user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    identity = (
        db.query(AuthIdentity).filter_by(user_id=user.id, provider="password").first()
    )

    if (
        not identity
        or not identity.password
        or not check_password(form_data.password, identity.password)
    ):
        logger.warning(f"Failed password attempt for user: {user.id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=str(user.id), role=user.role)
    return LoginTokenResponse(access_token=access_token, token_type="bearer")


@router.post(
    "/login/{provider}",
    status_code=status.HTTP_200_OK,
    response_model=LoginTokenResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": HTTPError,
            "description": "Invalid Google token or user not found",
        },
    },
)
def login_provider(
    provider: AuthProviderEnum,
    token: ProviderTokenResponse,
    db: Session = Depends(get_db),
) -> LoginTokenResponse:
    p = {
        provider.GOOGLE: get_google_user,
    }
    user = p[provider](db, token.token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    access_token = create_access_token(subject=str(user.id), role=user.role)

    return LoginTokenResponse(access_token=access_token, token_type="bearer")


@router.get(
    "/verify-email",
    response_model=MessageResponse,
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
    db: SessionDep,
    token: str,
) -> MessageResponse:
    """Endpoint to verify a user's email using a token."""
    email = verify_email_verification_token(
        token, settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS
    )
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

    return MessageResponse(message="Email successfully verified")


@router.post(
    "/logout",
    response_model=MessageResponse,
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
    """Endpoint to log out a user by blacklisting their JWT token."""
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


@router.post(
    "/password-recovery/{email}",
    status_code=status.HTTP_200_OK,
    response_model=MessageResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": HTTPError,
            "description": "User not found",
        },
    },
)
async def password_recovery(email: EmailStr, db: SessionDep) -> MessageResponse:
    """Endpoint to initiate password recovery by sending an OTP to the user's email."""
    # Check if user exists
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    await send_reset_password_email(NameEmail(email=email, name=email))

    return MessageResponse(message="Password recovery email sent")


@router.post(
    "/verify-otp",
    status_code=status.HTTP_200_OK,
    response_model=VerifyOTPResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": HTTPError,
            "description": "Invalid or expired OTP",
        },
    },
)
async def verify_otp(otp_request: OTPRequest) -> VerifyOTPResponse:
    """Endpoint to verify the OTP sent to the user's email for password recovery."""
    is_valid_with_token = await verify_otp_and_generate_token(
        otp_request.email, otp_request.otp
    )

    if not is_valid_with_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP",
        )

    return VerifyOTPResponse(
        message="OTP verified successfully", token=is_valid_with_token
    )


@router.post(
    "/password-reset",
    status_code=status.HTTP_200_OK,
    response_model=MessageResponse,
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
async def password_reset(
    request: PasswordResetRequest,
    db: SessionDep,
) -> MessageResponse:
    """Endpoint to reset the user's password using a valid token."""
    is_verified = await verify_password_reset_token(request.email, request.token)
    if not is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token",
        )

    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    identity = (
        db.query(AuthIdentity).filter_by(user_id=user.id, provider="password").first()
    )
    if not identity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Password authentication method not found for user",
        )

    # Update the user's password
    identity.password = get_password_hash(request.new_password)
    db.commit()

    return MessageResponse(message="Password successfully reset")
