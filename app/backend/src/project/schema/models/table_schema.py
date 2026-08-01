from __future__ import annotations

import uuid

from project.schema.schema import BaseSchema


class TableSchema(BaseSchema):
    """
    This model represents a table in the system.
    """

    id: uuid.UUID | None = None
    name: str
