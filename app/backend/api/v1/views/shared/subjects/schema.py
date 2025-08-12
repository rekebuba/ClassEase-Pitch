from typing import List

from extension.pydantic.models.grade_schema import (
    GradeWithRelatedSchema,
)
from extension.pydantic.models.subject_schema import (
    SubjectSchema,
    SubjectWithRelatedSchema,
)


class SubjectLightSchema(SubjectSchema):
    grades: List[GradeWithRelatedSchema] = []
