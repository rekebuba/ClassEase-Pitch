from __future__ import annotations

import uuid

from project.schema.schema import BaseSchema


class BlacklistTokenSchema(BaseSchema):
    """
    This model represents a blacklisted token in the system.
    """

    id: uuid.UUID | None = None
    jti: str
