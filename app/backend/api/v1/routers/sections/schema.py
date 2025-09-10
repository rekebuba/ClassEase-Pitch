import uuid

from pydantic import BaseModel, ConfigDict

from utils.utils import to_camel


class SectionFilterParams(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    grade_id: uuid.UUID
    q: str | None = None
