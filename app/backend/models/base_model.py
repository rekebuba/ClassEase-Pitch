#!/usr/bin/python3
""" Module for BaseModel class """

from dataclasses import InitVar, asdict, dataclass, field
from datetime import date, datetime
import models
from enum import Enum
from sqlalchemy import String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, DeclarativeBase, DeclarativeMeta, MappedAsDataclass, Mapped, mapped_column
import uuid
import bcrypt
from sqlalchemy.sql import func
from typing import Type
from enum import Enum as PythonEnum


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


class CustomTypes:
    class RoleEnum(PythonEnum):
        ADMIN = "admin"
        TEACHER = "teacher"
        STUDENT = "student"


@dataclass
class BaseModel(MappedAsDataclass, Base, CustomTypes):
    """Defines all common attributes/methods for other classes"""

    __abstract__ = True  # Prevents SQLAlchemy from creating a table for this class

    # Dataclass fields (not mapped to SQLAlchemy)
    id: Mapped[str] = mapped_column(
        String(36),  # UUIDs are 36 characters long
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        init=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default_factory=datetime.utcnow,
        init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default_factory=datetime.utcnow,
        onupdate=func.now(),  # Automatically update on modification
        init=False
    )

    def save(self):
        """Saves the current instance to the storage."""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Converts the instance to a dictionary representation."""
        data = asdict(self)

        # Handle Enum fields
        for key, value in data.items():
            if isinstance(value, Enum):
                data[key] = value.value
            if isinstance(value, datetime):
                data[key] = value.strftime('%Y-%m-%dT%H:%M:%S.%f')
            if isinstance(value, date):
                data[key] = value.strftime('%Y-%m-%d')

        return data

    def delete(self):
        """Delete the current instance from storage."""
        models.storage.delete(self)

    def __str__(self):
        """Returns a string representation of the instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.to_dict()}"
