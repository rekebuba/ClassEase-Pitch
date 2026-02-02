from __future__ import annotations

import uuid

from pydantic import BaseModel, ConfigDict

from project.utils.utils import to_camel


class BlacklistTokenSchema(BaseModel):
    """
    This model represents a blacklisted token in the system.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID | None = None
    jti: str
