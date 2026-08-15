import uuid
from typing import List, Optional

from pydantic import Field

from project.schema.models import SectionSchema
from project.schema.models.grade_schema import GradeSchema
from project.schema.models.stream_schema import StreamSchema
from project.schema.models.subject_schema import (
    SubjectSchema,
)
from project.schema.schema import BaseSchema
from project.utils.enum import GradeEnum, GradeLevelEnum


class UpdateGrade(BaseSchema):
    """
    This model represents a grade  that can be updated in the system.
    """

    grade: Optional[GradeEnum] = Field(default=None)
    level: Optional[GradeLevelEnum] = Field(default=None)
    has_stream: Optional[bool] = Field(default=None)


class UpdateStream(BaseSchema):
    """
    This model represents a stream in the system that can be updated.
    """

    id: uuid.UUID
    name: Optional[str] = Field(default=None)


class UpdateSubject(BaseSchema):
    """
    This model represents a subject that can be updated in the system.
    """

    id: uuid.UUID
    name: str
    code: str


class UpdateSection(BaseSchema):
    """
    This model represents a section in the system that can be updated.
    """

    id: uuid.UUID
    section: str


class StreamSetupSchema(StreamSchema):
    subjects: List[SubjectSchema]


class GradeStreamSetup(BaseSchema):
    id: uuid.UUID
    stream: StreamSchema | None
    subjects: List[SubjectSchema]


class UpdateStreamSetup(UpdateStream):
    subjects: List[UpdateSubject]


class GradeSetupSchema(GradeSchema):
    grade_streams: List[GradeStreamSetup]
    sections: List[SectionSchema]


class UpdateGradeSetup(UpdateGrade):
    """Update Grade Setup Schema"""

    subjects: Optional[List[UpdateSubject]] = Field(default=None)
    streams: Optional[List[UpdateStreamSetup]] = Field(default=None)
    sections: Optional[List[UpdateSection]] = Field(default=None)


class UpdateGradeSetupSuccess(BaseSchema):
    message: str = Field(default="Grade Setup updated Successfully")


class DeleteGradeSetupSuccess(BaseSchema):
    message: str = Field(default="Grade Setup Deleted Successfully")


class NewGrade(BaseSchema):
    grade: GradeEnum
    level: GradeLevelEnum
    has_stream: bool


class NewGradeSuccess(BaseSchema):
    id: uuid.UUID
    message: str = Field(default="Grade created Successfully")
