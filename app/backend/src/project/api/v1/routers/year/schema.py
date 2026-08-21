import uuid
from datetime import date
from typing import Optional

from pydantic import Field, model_validator

from project.schema.models.year_schema import YearSchema
from project.schema.schema import BaseSchema
from project.utils.enum import (
    AcademicTermTypeEnum,
    AcademicYearStatusEnum,
)
from project.utils.type import SetupMethodType


class YearSummary(YearSchema):
    pass


class NewYear(BaseSchema):
    """
    This model represents a new year to be created in the system.
    """

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
        if self.setup_methods != "Last Year Copy" and self.copy_from_year_id is not None:
            raise ValueError(
                "copy_from_year_id must be None \
                unless setup_methods is 'Last Year Copy'"
            )
        return self


class DeleteYearSuccess(BaseSchema):
    message: str = Field(default="Year deleted Successfully")
