from __future__ import annotations
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from flask import url_for
from pydantic import BaseModel, ConfigDict, Field

from api.v1.views.utils import generate_token
from extension.enums.enum import GradeLevelEnum
from extension.functions.helper import to_camel
from extension.pydantic.hal_link.link_schema import Link
from models.grade import Grade

if TYPE_CHECKING:
    from .teacher_schema import TeacherSchema
    from .stream_schema import StreamSchema
    from .yearly_subject_schema import YearlySubjectSchema
    from .student_year_record_schema import StudentYearRecordSchema
    from .student_schema import StudentSchema


class GradeSchema(BaseModel):
    """
    This model represents a grade in the system. It inherits from BaseModel.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    grade: str
    level: GradeLevelEnum
    links: Dict[str, Link] = Field(alias="_links")

    @classmethod
    @generate_token
    def hal_form(cls, grade: Grade, token: str) -> Dict[str, Any]:
        # add the _links field
        links = {
            "self": Link(
                href=url_for("auths.get_subject_by_id", grade_id=token),
                method="GET",
            )
        }

        setattr(grade, "_links", links)
        base_model = cls.model_validate(grade).model_dump(by_alias=True)

        return base_model


class GradeRelationshipSchema(BaseModel):
    """This model represents the relationships of a GradeSchema.
    It is used to define the relationships between the GradeSchema and other schemas.
    """

    teachers: Optional[List[TeacherSchema]]
    streams: Optional[List[StreamSchema]]
    yearly_subjects: Optional[List[YearlySubjectSchema]]
    student_year_records: Optional[List[StudentYearRecordSchema]]
    students: Optional[List["StudentSchema"]] = None
