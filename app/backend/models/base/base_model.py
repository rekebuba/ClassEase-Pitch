#!/usr/bin/python3
"""Module for BaseModel class"""

import uuid
from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
)
from sqlalchemy.sql import func

import models
from models.base.column_type import AwareDateTime, UUIDType


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
        UUIDType(),
        default_factory=uuid.uuid4,
        primary_key=True,
        init=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        AwareDateTime,
        default_factory=lambda: datetime.now(timezone.utc),
        server_default=func.now(),  # let DB insert UTC
        init=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        AwareDateTime,
        default_factory=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        onupdate=func.now(),
        init=False,
    )

    def save(self) -> None:
        """Saves the current instance to the storage."""
        self.updated_at = datetime.now(timezone.utc)
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, **kwargs: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Converts the instance to a dictionary representation."""
        data = asdict(self)

        # Handle Enum fields
        for key, value in data.items():
            if isinstance(value, Enum):
                data[key] = value.value
            if isinstance(value, datetime):
                if "time" in key:
                    data[key] = value.strftime("%H:%M:%S")
                else:
                    data[key] = value.strftime("%Y-%m-%d")
            elif isinstance(value, date):
                data[key] = value.strftime("%Y-%m-%d")

        return data

    def delete(self) -> None:
        """Delete the current instance from storage."""
        models.storage.delete(self)

    def __str__(self) -> str:
        """Returns a string representation of the instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.to_dict()}"
