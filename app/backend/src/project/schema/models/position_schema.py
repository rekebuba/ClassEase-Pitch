import uuid

from pydantic import AwareDatetime

from project.schema.schema import BaseSchema


class PositionSchema(BaseSchema):
    id: uuid.UUID
    title: str
    department_id: uuid.UUID
    created_at: AwareDatetime
    updated_at: AwareDatetime
