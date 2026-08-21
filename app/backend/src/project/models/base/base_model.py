#!/usr/bin/python3
"""Module for BaseModel class"""

import uuid
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import UUID, DateTime, MetaData
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
)
from sqlalchemy.sql import func

POSTGRES_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    """
    The use of naming_convention:
        Alembic needs names to track, drop, or alter constraints.

        The Conflict: If you manually name a constraint in your code,
        but the database already has a constraint (auto-generated one),
        Alembic will try to "create" it and fail.
    more info: https://alembic.sqlalchemy.org/en/latest/autogenerate.html
    """

    metadata = MetaData(naming_convention=POSTGRES_CONVENTION)


@dataclass
class TimestampMixin(MappedAsDataclass, Base):
    """Mixin for models that need created_at and updated_at."""

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        init=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        init=False,
    )


@dataclass
class BaseModel(TimestampMixin):
    """Base class for entities with a standard UUID surrogate primary key."""

    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        default_factory=uuid.uuid4,
        primary_key=True,
        init=False,
    )

    def __str__(self) -> str:
        """Returns a string representation of the instance."""
        return f"[{self.__class__.__name__}]: ({self.id})]"
