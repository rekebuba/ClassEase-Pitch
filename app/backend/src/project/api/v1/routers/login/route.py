import logging
from typing import Annotated, Any, Dict

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from project.api.v1.routers.dependencies import SessionDep, TokenDep, get_db
from project.core.config import settings
from project.core.security import ALGORITHM, check_password, create_access_token
from project.models.blacklist_token import BlacklistToken
from project.models.user import User

from .schema import LogOutResponse, Token

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token, operation_id="login_credential")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    user = db.query(User).filter(User.identification == form_data.username).first()

    if not user:
        logger.warning(f"Login attempt for non-existent user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect identification or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not check_password(form_data.password, user.password):
        logger.warning(f"Failed password attempt for user: {user.id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect identification or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=str(user.id), role=user.role)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout", response_model=LogOutResponse)
async def logout(
    token: TokenDep,
    db: SessionDep,
) -> Dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
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
