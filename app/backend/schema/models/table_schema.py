from __future__ import annotations

import uuid

from pydantic import BaseModel, ConfigDict

from utils.utils import to_camel


class TableSchema(BaseModel):
    """
    This model represents a table in the system.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID | None = None
    name: str
