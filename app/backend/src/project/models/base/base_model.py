#!/usr/bin/python3
"""Module for BaseModel class"""

import uuid
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import UUID, DateTime
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
)
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


@dataclass
class AssociationBase(Base):
    __abstract__ = True


@dataclass
class BaseModel(MappedAsDataclass, Base):
    """Defines all common attributes/methods for other classes"""

    __abstract__ = True  # Prevents SQLAlchemy from creating a table for this class

    # Dataclass fields (not mapped to SQLAlchemy)
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        default_factory=uuid.uuid4,
        primary_key=True,
        init=False,
    )
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

    def __str__(self) -> str:
        """Returns a string representation of the instance."""
        return f"[{self.__class__.__name__}]: ({self.id})]"
