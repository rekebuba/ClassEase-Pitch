import uuid
from datetime import date
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from project.schema.models.year_schema import YearSchema
from project.utils.enum import (
    AcademicTermTypeEnum,
    AcademicYearStatusEnum,
    GradeEnum,
    GradeLevelEnum,
)
from project.utils.type import SetupMethodType
from project.utils.utils import to_camel


class YearSummary(YearSchema):
    pass


class NewYear(BaseModel):
    """
    This model represents a new year to be created in the system.
    """

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    name: str
    calendar_type: AcademicTermTypeEnum
    status: AcademicYearStatusEnum
    start_date: date
    end_date: date
    setup_methods: SetupMethodType
    copy_from_year_id: Optional[uuid.UUID] = Field(default=None)

    @model_validator(mode="after")
    def validate_copy_from_year(self) -> "NewYear":
        if self.setup_methods == "Last Year Copy" and self.copy_from_year_id is None:
            raise ValueError(
                "copy_from_year_id must be provided \
                when setup_methods is 'Last Year Copy'"
            )
        if (
            self.setup_methods != "Last Year Copy"
            and self.copy_from_year_id is not None
        ):
            raise ValueError(
                "copy_from_year_id must be None \
                unless setup_methods is 'Last Year Copy'"
            )
        return self


class NewYearSuccess(BaseModel):
    id: uuid.UUID
    message: str = Field(default="Year created Successfully")


class DeleteYearSuccess(BaseModel):
    message: str = Field(default="Year deleted Successfully")


class SubjectTemplate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    name: str
    code: str


class SectionTemplate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    section: str


class StreamTemplate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    name: str
    subjects: List[SubjectTemplate]


class GradeTemplate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    grade: GradeEnum
    level: GradeLevelEnum
    has_stream: bool
    subjects: List[SubjectTemplate]
    streams: List[StreamTemplate]


class YearSetupTemplate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    subjects: List[SubjectTemplate]
    sections: List[SectionTemplate]
    grades: List[GradeTemplate]
