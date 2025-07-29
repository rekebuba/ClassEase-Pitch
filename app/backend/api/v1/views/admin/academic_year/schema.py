from datetime import date
from typing import List
from pydantic import BaseModel, ConfigDict

from extension.enums.enum import AcademicTermTypeEnum
from extension.functions.helper import to_camel
from extension.pydantic.models.academic_term_schema import AcademicTermSchema
from extension.pydantic.models.grade_schema import GradeSchema
from extension.pydantic.models.section_schema import SectionSchema
from extension.pydantic.models.stream_schema import StreamSchema
from extension.pydantic.models.subject_schema import SubjectSchema


class YearDetailSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    calendar_type: AcademicTermTypeEnum
    academic_year: str
    ethiopian_year: str
    gregorian_year: str
    start_date: date
    end_date: date


class NestedGradeSetupSchema(GradeSchema):
    streams: List[StreamSchema] | None = None
    sections: List[SectionSchema]
    subjects: SubjectSchema


class AcademicYearSetupSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    year: YearDetailSchema
    academic_term: AcademicTermSchema
    subjects: List[SubjectSchema]
    grades: List[NestedGradeSetupSchema]
