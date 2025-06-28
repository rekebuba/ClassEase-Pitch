from __future__ import annotations
from typing import TYPE_CHECKING, List
from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from .teacher_schema import TeacherSchema


class SubjectSchema(BaseModel):
    """
    This model represents a subject in the system. It inherits from BaseModel.
    """
    model_config = ConfigDict(from_attributes=True)
    

    name: str


class SubjectRelationshipSchema(BaseModel):
    """This model represents the relationships of a SubjectSchema.
    It is used to define the relationships between the SubjectSchema and other schemas.
    """

    teachers: List[TeacherSchema]
