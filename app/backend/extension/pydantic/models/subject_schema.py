from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
from pydantic import BaseModel, ConfigDict
from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .teacher_schema import TeacherSchema
    from .yearly_subject_schema import YearlySubjectSchema


class SubjectSchema(BaseModel):
    """
    This model represents a subject in the system. It inherits from BaseModel.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: str | None = None
    name: str


class SubjectRelationshipSchema(BaseModel):
    """This model represents the relationships of a SubjectSchema.
    It is used to define the relationships between the SubjectSchema and other schemas.
    """

    teachers: Optional[List[TeacherSchema]]
    yearly_subjects: Optional[List[YearlySubjectSchema]]
