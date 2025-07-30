from datetime import date
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from extension.enums.enum import (
    AcademicTermEnum,
    AcademicTermTypeEnum,
    AcademicYearStatusEnum,
    GradeLevelEnum,
)
from extension.functions.helper import to_camel


class YearDetailSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    calendar_type: AcademicTermTypeEnum
    name: str
    start_date: date
    end_date: date
    status: AcademicYearStatusEnum


class AcademicTermDetail(BaseModel):
    """
    This model represents an academic term in the system.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    name: AcademicTermEnum
    start_date: date
    end_date: date
    registration_start: Optional[date] = None
    registration_end: Optional[date] = None

class StreamDetailSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )
    
    name: str
    subjects: List[str]

class NestedGradeSetupSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    grade: str
    level: GradeLevelEnum
    has_stream: bool = False
    streams: List[StreamDetailSchema] | None = None
    sections: List[str]
    subjects: List[str]


class AcademicYearSetupSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    year: YearDetailSchema
    academic_term: List[AcademicTermDetail]
    subjects: List[str]
    grades: List[NestedGradeSetupSchema]
