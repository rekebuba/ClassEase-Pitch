import uuid
from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict

from extension.functions.helper import to_camel


class FilterParams(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    year_id: uuid.UUID
    q: str | None = None


# JSON Patch specific schemas
class JSONPatchOperation(BaseModel):
    op: Literal["add", "remove", "replace", "move", "copy", "test"]
    path: str
    value: Optional[Any] = None


class JSONPatchRequest(BaseModel):
    patch: list[JSONPatchOperation]
