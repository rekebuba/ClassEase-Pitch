import uuid
from typing import Any, Literal, Optional

from project.schema.schema import BaseSchema


class FilterParams(BaseSchema):
    year_id: uuid.UUID
    q: str | None = None


class SearchParams(BaseSchema):
    q: str | None = None


# JSON Patch specific schemas
class JSONPatchOperation(BaseSchema):
    op: Literal["add", "remove", "replace", "move", "copy", "test"]
    path: str
    value: Optional[Any] = None


class JSONPatchRequest(BaseSchema):
    patch: list[JSONPatchOperation]


class HTTPError(BaseSchema):
    """
    HTTP error schema to be used when an HTTPException is thrown.
    """

    detail: str
