from project.schema.models import GradeSchema, StreamSchema
from project.schema.schema import BaseSchema


class GradeStreamSchema(BaseSchema):
    stream: StreamSchema | None
    grade: GradeSchema
