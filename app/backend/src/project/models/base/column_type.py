#!/usr/bin/python3
"""Module for BaseModel class"""

import uuid
from datetime import datetime, timezone
from typing import Optional, Union

from sqlalchemy import BINARY, DateTime, Dialect, TypeDecorator


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
