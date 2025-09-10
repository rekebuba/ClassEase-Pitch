import uuid
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from schema.models.grade_schema import GradeSchema
from schema.models.section_schema import (
    SectionSchema,
)
from schema.models.stream_schema import StreamSchema
from schema.models.subject_schema import (
    SubjectSchema,
)
from utils.enum import GradeEnum, GradeLevelEnum
from utils.utils import to_camel


class UpdateGrade(BaseModel):
    """
    This model represents a grade  that can be updated in the system.
    """

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    grade: Optional[GradeEnum] = Field(default=None)
    level: Optional[GradeLevelEnum] = Field(default=None)
    has_stream: Optional[bool] = Field(default=None)


class UpdateStream(BaseModel):
    """
    This model represents a stream in the system that can be updated.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    name: Optional[str] = Field(default=None)


class UpdateSubject(BaseModel):
    """
    This model represents a subject that can be updated in the system.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    name: str
    code: str


class UpdateSection(BaseModel):
    """
    This model represents a section in the system that can be updated.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    section: str


class StreamSetupSchema(StreamSchema):
    subjects: List[SubjectSchema]


class UpdateStreamSetup(UpdateStream):
    subjects: List[UpdateSubject]


class GradeSetupSchema(GradeSchema):
    subjects: List[SubjectSchema]
    streams: List[StreamSetupSchema]
    sections: List[SectionSchema]


class UpdateGradeSetup(UpdateGrade):
    """Update Grade Setup Schema"""

    subjects: Optional[List[UpdateSubject]] = Field(default=None)
    streams: Optional[List[UpdateStreamSetup]] = Field(default=None)
    sections: Optional[List[UpdateSection]] = Field(default=None)


class UpdateGradeSetupSuccess(BaseModel):
    message: str = Field(default="Grade Setup updated Successfully")


class DeleteGradeSetupSuccess(BaseModel):
    message: str = Field(default="Grade Setup Deleted Successfully")


class NewGrade(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    grade: GradeEnum
    level: GradeLevelEnum
    has_stream: bool
    year_id: uuid.UUID


class NewGradeSuccess(BaseModel):
    id: uuid.UUID
    message: str = Field(default="Grade created Successfully")
