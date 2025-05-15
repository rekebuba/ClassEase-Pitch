#!/usr/bin/python3
"""Module for BaseModel class"""

from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
import models
from enum import Enum
from sqlalchemy import String, DateTime
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    DeclarativeBase,
    MappedAsDataclass,
)
import uuid
from sqlalchemy.sql import func
from typing import Any, Dict, Optional, Type, TypeVar


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


EnumT = TypeVar("EnumT", bound=Enum)


class CustomTypes:
    class RoleEnum(Enum):
        ADMIN = "admin"
        TEACHER = "teacher"
        STUDENT = "student"

        @classmethod
        def enum_value(cls: Type[EnumT], value: str) -> EnumT:
            """Convert a string value to the corresponding Enum member."""
            if not isinstance(value, str):
                raise TypeError(f"Expected a string, got {type(value).__name__}")

            for member in cls:
                if member.value == value:
                    return member
            raise ValueError(f"{value!r} is not a valid {cls.__name__}")


@dataclass
class AssociationBase(Base):
    __abstract__ = True


@dataclass
class BaseModel(MappedAsDataclass, Base, CustomTypes):
    """Defines all common attributes/methods for other classes"""

    __abstract__ = True  # Prevents SQLAlchemy from creating a table for this class

    # Dataclass fields (not mapped to SQLAlchemy)
    id: Mapped[str] = mapped_column(
        String(36),  # UUIDs are 36 characters long
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        init=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default_factory=lambda: datetime.now(timezone.utc),
        init=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default_factory=lambda: datetime.now(timezone.utc),
        onupdate=func.now(),  # Automatically update on modification
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
