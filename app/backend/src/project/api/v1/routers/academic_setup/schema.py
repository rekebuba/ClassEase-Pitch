import uuid
from datetime import date
from typing import Optional

from pydantic import Field

from project.schema.blueprint_schema import BluePrintTemplate
from project.schema.schema import BaseSchema
from project.utils.enum import (
    AcademicTermEnum,
    GradeEnum,
    GradeLevelEnum,
)


class TermCreateSchema(BaseSchema):
    name: AcademicTermEnum
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    registration_start: Optional[date] = None
    registration_end: Optional[date] = None


class SubjectCreateSchema(BaseSchema):
    name: str = Field(..., max_length=50)
    code: str = Field(..., max_length=20)


class GradeCreateSchema(BaseSchema):
    grade: GradeEnum
    level: GradeLevelEnum
    has_stream: bool = False


class SectionCreateSchema(BaseSchema):
    grade_id: uuid.UUID
    section: str = Field(..., max_length=1)


class StreamCreateSchema(BaseSchema):
    grade_id: uuid.UUID
    name: str = Field(..., max_length=50)


class AssessmentSchemeCreateSchema(BaseSchema):
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=255)


class AssessmentComponentCreateSchema(BaseSchema):
    term_id: uuid.UUID
    assessment_scheme_id: uuid.UUID
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    weight: float
    max_score: float
    display_order: int = 0


class SubjectOfferingCreateSchema(BaseSchema):
    year_id: uuid.UUID
    subject_id: uuid.UUID
    grade_id: uuid.UUID
    stream_id: Optional[uuid.UUID] = None
    assessment_scheme_id: uuid.UUID


class ClassSectionCreateSchema(BaseSchema):
    academic_year_id: uuid.UUID
    section_id: uuid.UUID
    grade_id: uuid.UUID
    stream_id: Optional[uuid.UUID] = None


class ManualSetupBulkSchema(BaseSchema):
    year_id: uuid.UUID
    blueprint: BluePrintTemplate
