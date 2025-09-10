import uuid
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from schema.models.grade_schema import (
    GradeSchema,
)
from schema.models.stream_schema import StreamSchema
from schema.models.subject_schema import (
    SubjectSchema,
)
from utils.utils import to_camel


class SubjectSetupSchema(SubjectSchema):
    grades: List[GradeSchema]
    streams: List[StreamSchema]


class UpdateSubjectFields(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    name: Optional[str] = Field(default=None, min_length=3, max_length=50)
    code: Optional[str] = Field(default=None, min_length=3, max_length=10)


class UpdateSubjectGrade(BaseModel):
    id: uuid.UUID


class UpdateSubjectStream(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    grade_id: uuid.UUID


class UpdateSubjectSetup(UpdateSubjectFields):
    grades: Optional[List[UpdateSubjectGrade]] = Field(default=None)
    streams: Optional[List[UpdateSubjectStream]] = Field(default=None)


class UpdateSubjectSetupSuccess(BaseModel):
    message: str = Field(default="Subject Setup updated Successfully")


class NewSubject(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    name: str = Field(min_length=3, max_length=50)
    code: str = Field(min_length=3, max_length=10)
    year_id: uuid.UUID


class NewSubjectSuccess(BaseModel):
    id: uuid.UUID
    message: str = Field(default="Subject created Successfully")
