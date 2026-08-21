import uuid

from project.schema.schema import BaseSchema


class SectionFilterParams(BaseSchema):
    grade_id: uuid.UUID
    q: str | None = None
