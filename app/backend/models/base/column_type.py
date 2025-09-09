#!/usr/bin/python3
"""Module for BaseModel class"""

import uuid
from datetime import datetime, timezone
from typing import Optional, Union

from sqlalchemy import BINARY, DateTime, Dialect, TypeDecorator


class UUIDType(TypeDecorator[uuid.UUID]):
    """Custom SQLAlchemy type for storing UUID as BINARY(16) in MySQL."""

    impl: BINARY = BINARY(16)
    cache_ok = True  # Important for statement caching in SQLAlchemy 1.4+

    def process_bind_param(
        self, value: Union[uuid.UUID, str, bytes, None], dialect: Dialect
    ) -> Optional[bytes]:
        """Convert Python value to database value."""
        if value is None:
            return None
        if isinstance(value, uuid.UUID):
            return value.bytes
        if isinstance(value, str):
            return uuid.UUID(value).bytes
        if isinstance(value, bytes) and len(value) == 16:
            return value
        raise ValueError(f"Invalid UUID value: {value!r}")

    def process_result_value(
        self, value: Optional[bytes], dialect: Dialect
    ) -> Optional[uuid.UUID]:
        """Convert database value to Python value."""
        if value is not None:
            return uuid.UUID(bytes=value)
        return None

    def __repr__(self) -> str:
        return "UUIDType()"


class AwareDateTime(TypeDecorator[datetime]):
    """
    like datetime, with the constraint that the value must have timezone info
    """

    impl = DateTime(timezone=True)

    def process_bind_param(
        self, value: Optional[datetime], dialect: Dialect
    ) -> Optional[datetime]:
        if value is None:
            return None

        if not isinstance(value, datetime):
            raise TypeError("Expected datetime object")

        if value.tzinfo is None:
            # Convert naive to UTC-aware
            return value.replace(tzinfo=timezone.utc)
        else:
            # Convert any timezone to UTC for storage
            return value.astimezone(timezone.utc)

    def process_result_value(
        self, value: Optional[datetime], dialect: Dialect
    ) -> Optional[datetime]:
        # Ensure timezone-aware when loading
        if value is not None and value.tzinfo is None:
            # Ensure loaded values are timezone-aware
            return value.replace(tzinfo=timezone.utc)
        return value
