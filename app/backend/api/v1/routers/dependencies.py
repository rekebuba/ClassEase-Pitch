from collections.abc import Generator
from datetime import datetime, timezone
from typing import Annotated, Any, Dict, List, Type

import jwt
from fastapi import Depends, HTTPException, Query, status
from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordBearer,
)
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel, ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session

from core import security
from core.config import settings
from core.db import engine
from extension.enums.enum import RoleEnum
from extension.functions.helper import classify_model_fields, extract_inner_model
from extension.pydantic.schema import TokenPayload
from models.blacklist_token import BlacklistToken
from models.grade import Grade
from models.user import User

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
security_bearer = HTTPBearer(auto_error=True)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(
    session: SessionDep,
    token: TokenDep,
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if token_data.exp < datetime.now(timezone.utc):
            raise credentials_exception

        # Check if the token is blacklisted
        blacklisted = session.scalar(
            select(BlacklistToken).where(BlacklistToken.jti == str(token_data.jti))
        )

        if blacklisted:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is Black Listed try to Sign in to Continue",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    user = session.get(User, token_data.sub)
    if user is None:
        raise credentials_exception
    return user


class ProtectedRoute:
    def __init__(self, roles: List[RoleEnum] = []):
        self.roles = roles

    def __call__(
        self, current_user: Annotated[User, Depends(get_current_user)]
    ) -> User:
        if current_user.role not in self.roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return current_user


async def parse_nested_params(
    *,
    base_model: Type[BaseModel],
    prefix: str = "",
    expand: str,
    fields: str,
) -> Dict[str, Any]:
    """
    FastAPI dependency that recursively parses 'expand' and 'fields' query parameters
    into a nested dictionary that Pydantic's `model_dump(include=...)` can consume.

    Args:
        request: FastAPI request object
        base_model: The Pydantic model to parse parameters for
        prefix: Current nesting prefix (used internally for recursion)
        expand: The expand query parameter value
        fields: The fields query parameter value

    Returns:
        Dictionary suitable for Pydantic's model_dump(include=...)

    Raises:
        HTTPException: 400 if invalid fields or expansions are requested
    """
    expand_value = expand or ""
    fields_value = fields or ""

    # Filter only relevant expansions for this prefix
    expansions = {
        e[len(prefix) + 1 :] if prefix else e
        for e in expand_value.split(",")
        if e.strip() and (not prefix or e.startswith(prefix + ".") or e == prefix)
    }
    if expansions == {""}:
        expansions = set()

    # Filter only relevant fields for this prefix
    field_names = {
        f[len(prefix) + 1 :] if prefix else f
        for f in fields_value.split(",")
        if f.strip() and (not prefix or f.startswith(prefix + ".") or f == prefix)
    }
    if field_names == {""}:
        field_names = set()

    classified = classify_model_fields(base_model)
    allowed_fields = set(classified.get("model_class", []))

    valid_fields: List[str] = []
    for field in field_names:
        # Validate that the field is a model class
        if field == "all":
            valid_fields.extend(allowed_fields)
            break

        if ("." not in field and field not in allowed_fields) or (
            "." in field and not expansions
        ):
            # Nested field without expansion -> invalid
            allowed_fields.add("all")
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Invalid field requested",
                    "meta": {
                        "invalid_field": field,
                        "allowed_fields": list(allowed_fields),
                    },
                },
            )
        elif "." not in field:
            valid_fields.append(field)

    # If no fields explicitly given for this model, use defaults
    if not valid_fields:
        if hasattr(base_model, "default_fields"):
            valid_fields = list(base_model.default_fields())
        else:
            valid_fields = list(base_model.model_fields.keys())

    if "id" in base_model.model_fields:
        valid_fields.append("id")  # ensure id is always included

    include_dict: Dict[str, Any] = {f: ... for f in valid_fields}

    # Process expansions
    allowed_expansions = set(classified.get("model_sub_class", []))
    for exp in expansions:
        if exp == "":
            continue

        expand_field, rest = exp.split(".", 1) if "." in exp else (exp, None)

        # Validate that the expansion field is a model subclass
        if expand_field not in allowed_expansions:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Invalid expand requested",
                    "meta": {
                        "invalid_expand": expand_field,
                        "allowed_expansions": list(allowed_expansions),
                    },
                },
            )

        is_list, related_model = extract_inner_model(
            base_model.model_fields[expand_field].annotation
        )
        # Build nested prefix for child expansion
        child_prefix = f"{prefix}.{expand_field}" if prefix else expand_field

        # Recursive call for nested expansion
        nested_params = await parse_nested_params(
            base_model=related_model,
            prefix=child_prefix,
            expand=expand,
            fields=fields,
        )

        include_dict[expand_field] = (
            {"__all__": nested_params} if is_list else nested_params
        )

    return include_dict


class NestedParamsDependency:
    def __init__(self, base_model: Type[BaseModel]):
        self.base_model = base_model

    async def __call__(
        self,
        expand: str = Query("", alias="expand"),
        fields: str = Query("", alias="fields"),
    ) -> Dict[str, Any]:
        try:
            return await parse_nested_params(
                base_model=self.base_model, expand=expand, fields=fields
            )
        except HTTPException as e:
            raise e

