from __future__ import annotations
from pydantic import BaseModel, ConfigDict

from extension.functions.helper import to_camel


class TableSchema(BaseModel):
    """
    This model represents a table in the system.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: str | None = None
    name: str
