from collections.abc import AsyncGenerator
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Annotated, Any, Dict, List, Set, Type

import jwt
from fastapi import Depends, HTTPException, Query, status
from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordBearer,
)
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel, ValidationError
from redis.asyncio import Redis
from sqlalchemy import event, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import Session, with_loader_criteria

from project.core import security
from project.core.access_control import (
    get_membership_with_roles,
    resolve_membership_permissions,
    resolve_membership_role_names,
    resolve_shell_role_from_names,
)
from project.core.config import settings
from project.core.db import engine, init_db
from project.core.tenant import (
    bind_db_school_context,
    get_current_school_id,
    set_current_membership_id,
    set_current_school_id,
)
from project.models.auth_session import AuthSession
from project.models.base.school_mixin import SchoolScopedMixin
from project.models.blacklist_token import BlacklistToken
from project.models.school_membership import SchoolMembership
from project.models.user import User
from project.schema.schema import TokenPayload
from project.utils.enum import RoleEnum, SchoolMembershipStatusEnum
from project.utils.utils import classify_model_fields, extract_inner_model

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
security_bearer = HTTPBearer(auto_error=True)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@event.listens_for(Session, "do_orm_execute")
def _apply_school_scope(execute_state):
    school_id = get_current_school_id()
    if (
        school_id is None
        or not execute_state.is_select
        or execute_state.execution_options.get("skip_school_scope")
    ):
        return

    execute_state.statement = execute_state.statement.options(
        with_loader_criteria(
            SchoolScopedMixin,
            lambda cls: cls.school_id == school_id,
            include_aliases=True,
        )
    )


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        await init_db(session)
        yield session


async def get_redis() -> AsyncGenerator[Redis, None]:
    redis_client = Redis.from_url(str(settings.REDIS_URL), decode_responses=True)
    yield redis_client


SessionDep = Annotated[AsyncSession, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]
RedisDep = Annotated[Redis, Depends(get_redis)]


@dataclass
class AuthenticatedActor:
    user: User
    membership: SchoolMembership
    auth_session: AuthSession
    permissions: Set[str]
    shell_role: RoleEnum


async def get_current_actor(
    session: SessionDep,
    token: TokenDep,
) -> AuthenticatedActor:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[security.ALGORITHM],
        )
        token_data = TokenPayload(**payload)

        if token_data.exp < datetime.now(timezone.utc):
            raise credentials_exception

        # Check if the token is blacklisted
        blacklisted = (
            await session.execute(
                select(BlacklistToken).where(BlacklistToken.jti == str(token_data.jti))
            )
        ).scalar_one_or_none()

        if blacklisted:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is Black Listed try to Sign in to Continue",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except (InvalidTokenError, ValidationError):
        raise credentials_exception

    if (
        token_data.school_id is None
        or token_data.membership_id is None
        or token_data.session_id is None
    ):
        raise credentials_exception

    set_current_school_id(token_data.school_id)
    membership = await get_membership_with_roles(session, token_data.membership_id)
    if (
        membership is None
        or str(membership.user_id) != token_data.sub
        or membership.school_id != token_data.school_id
        or membership.status != SchoolMembershipStatusEnum.ACTIVE
    ):
        raise credentials_exception

    auth_session = await session.get(AuthSession, token_data.session_id)
    if (
        auth_session is None
        or auth_session.membership_id != membership.id
        or auth_session.user_id != membership.user_id
        or auth_session.revoked_at is not None
        or auth_session.expires_at <= datetime.now(timezone.utc)
    ):
        raise credentials_exception

    if token_data.permissions_version != membership.permissions_version:
        raise credentials_exception

    await bind_db_school_context(session, membership.school_id)
    set_current_membership_id(membership.id)

    permissions = resolve_membership_permissions(membership)
    shell_role = resolve_shell_role_from_names(
        resolve_membership_role_names(membership),
        fallback=membership.user.role,
    )

    return AuthenticatedActor(
        user=membership.user,
        membership=membership,
        auth_session=auth_session,
        permissions=permissions,
        shell_role=shell_role,
    )


async def get_current_user(
    current_actor: Annotated[AuthenticatedActor, Depends(get_current_actor)],
) -> User:
    return current_actor.user


class ProtectedRoute:
    def __init__(self, roles: List[RoleEnum] = []):
        self.roles = roles

    def __call__(
        self, current_actor: Annotated[AuthenticatedActor, Depends(get_current_actor)]
    ) -> AuthenticatedActor:
        if current_actor.shell_role not in self.roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return current_actor


shared_route = Annotated[
    AuthenticatedActor,
    Depends(ProtectedRoute([RoleEnum.ADMIN, RoleEnum.TEACHER, RoleEnum.STUDENT])),
]
admin_route = Annotated[AuthenticatedActor, Depends(ProtectedRoute([RoleEnum.ADMIN]))]
student_route = Annotated[
    AuthenticatedActor,
    Depends(ProtectedRoute([RoleEnum.ADMIN, RoleEnum.STUDENT])),
]
teacher_route = Annotated[
    AuthenticatedActor,
    Depends(ProtectedRoute([RoleEnum.ADMIN, RoleEnum.TEACHER])),
]


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
            valid_fields = list(base_model.default_fields())  # type: ignore
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
