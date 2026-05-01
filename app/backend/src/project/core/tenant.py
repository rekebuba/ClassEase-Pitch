from __future__ import annotations

import uuid
from contextvars import ContextVar, Token
from dataclasses import dataclass

from fastapi import Request
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

_current_school_id: ContextVar[uuid.UUID | None] = ContextVar(
    "current_school_id",
    default=None,
)
_current_membership_id: ContextVar[uuid.UUID | None] = ContextVar(
    "current_membership_id",
    default=None,
)
_request_school_slug: ContextVar[str | None] = ContextVar(
    "request_school_slug",
    default=None,
)


@dataclass
class TenantContextTokens:
    school_id: Token[uuid.UUID | None]
    membership_id: Token[uuid.UUID | None]
    school_slug: Token[str | None]


def get_current_school_id() -> uuid.UUID | None:
    return _current_school_id.get()


def get_current_membership_id() -> uuid.UUID | None:
    return _current_membership_id.get()


def get_request_school_slug() -> str | None:
    return _request_school_slug.get()


def set_current_school_id(value: uuid.UUID | None) -> Token[uuid.UUID | None]:
    return _current_school_id.set(value)


def set_current_membership_id(value: uuid.UUID | None) -> Token[uuid.UUID | None]:
    return _current_membership_id.set(value)


def set_request_school_slug(value: str | None) -> Token[str | None]:
    return _request_school_slug.set(value)


def resolve_school_slug_from_request(request: Request) -> str | None:
    for header in ("x-school-slug", "x-tenant-slug"):
        value = request.headers.get(header)
        if value:
            return value.strip().lower()

    host = request.url.hostname or request.headers.get("host", "").split(":")[0]
    if not host:
        return None
    if host in {"localhost", "127.0.0.1"}:
        return None

    host_parts = host.split(".")
    if len(host_parts) < 3:
        return None

    subdomain = host_parts[0].strip().lower()
    if subdomain in {"www", "api"}:
        return None

    return subdomain


def reset_tenant_context(tokens: TenantContextTokens) -> None:
    _current_school_id.reset(tokens.school_id)
    _current_membership_id.reset(tokens.membership_id)
    _request_school_slug.reset(tokens.school_slug)


async def bind_db_school_context(
    session: AsyncSession,
    school_id: uuid.UUID | None,
) -> None:
    """Expose the active tenant to PostgreSQL RLS policies when available."""
    value = str(school_id) if school_id is not None else ""
    await session.execute(
        text("SELECT set_config('app.current_school_id', :school_id, true)"),
        {"school_id": value},
    )
