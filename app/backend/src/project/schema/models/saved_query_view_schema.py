from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any, Dict, Optional

from project.schema.schema import BaseSchema
from project.utils.enum import TableEnum

if TYPE_CHECKING:
    from project.schema.models.user_schema import UserSchema


class SavedQueryViewSchema(BaseSchema):
    """
    This model represents a saved query view in the system.
    """

    id: uuid.UUID | None = None
    user_id: uuid.UUID
    name: str
    table_name: TableEnum
    query_json: Dict[str, Any]


class SavedQueryViewRelatedSchema(BaseSchema):
    """This model represents the relationships of a SavedQueryViewSchema."""

    user: Optional[UserSchema] = None
