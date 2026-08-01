import uuid
from typing import List, Optional

from pydantic import Field

from project.schema.models.grade_schema import (
    GradeSchema,
)
from project.schema.models.stream_schema import StreamSchema
from project.schema.models.subject_schema import (
    SubjectSchema,
)
from project.schema.schema import BaseSchema


class SubjectSetupSchema(SubjectSchema):
    grades: List[GradeSchema]
    streams: List[StreamSchema]


class UpdateSubjectFields(BaseSchema):
    name: Optional[str] = Field(default=None, min_length=3, max_length=50)
    code: Optional[str] = Field(default=None, min_length=3, max_length=10)


class UpdateSubjectGrade(BaseSchema):
    id: uuid.UUID


class UpdateSubjectStream(BaseSchema):
    id: uuid.UUID
    grade_id: uuid.UUID


class UpdateSubjectSetup(UpdateSubjectFields):
    grades: Optional[List[UpdateSubjectGrade]] = Field(default=None)
    streams: Optional[List[UpdateSubjectStream]] = Field(default=None)


class UpdateSubjectSetupSuccess(BaseSchema):
    message: str = Field(default="Subject Setup updated Successfully")


class NewSubject(BaseSchema):
    name: str = Field(min_length=3, max_length=50)
    code: str = Field(min_length=3, max_length=10)
    year_id: uuid.UUID


class NewSubjectSuccess(BaseSchema):
    id: uuid.UUID
    message: str = Field(default="Subject created Successfully")
