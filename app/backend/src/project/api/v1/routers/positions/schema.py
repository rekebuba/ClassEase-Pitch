import uuid

from project.schema.schema import BaseSchema


class PositionBase(BaseSchema):
    title: str
    department_id: uuid.UUID
