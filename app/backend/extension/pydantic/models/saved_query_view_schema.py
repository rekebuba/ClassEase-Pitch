from __future__ import annotations
import uuid
from typing import TYPE_CHECKING, Optional, Any, Dict
from pydantic import BaseModel, ConfigDict

from extension.enums.enum import TableEnum
from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .user_schema import UserSchema


class SavedQueryViewSchema(BaseModel):
    """
    This model represents a saved query view in the system.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID | None = None
    user_id: uuid.UUID
    name: str
    table_name: TableEnum
    query_json: Dict[str, Any]


class SavedQueryViewRelatedSchema(BaseModel):
    """This model represents the relationships of a SavedQueryViewSchema."""

    user: Optional[UserSchema] = None
