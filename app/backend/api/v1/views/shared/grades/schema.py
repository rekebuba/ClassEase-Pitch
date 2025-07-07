from pydantic import BaseModel
from extension.pydantic.models.grade_schema import GradeSchema


class GradeResponse(BaseModel):
    grades: list[GradeSchema]
