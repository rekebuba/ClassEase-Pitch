#!/usr/bin/python3
"""Module for BaseModel class"""

from sqlalchemy import BINARY, Dialect, TypeDecorator
import uuid
from typing import Optional, Union


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
