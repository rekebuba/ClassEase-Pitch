from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
from pydantic import BaseModel, ConfigDict

from models.base_model import CustomTypes

if TYPE_CHECKING:
    from .teacher_schema import TeacherSchema


class GradeSchema(BaseModel):
    """
    This model represents a grade in the system. It inherits from BaseModel.
    """

    model_config = ConfigDict(from_attributes=True)

    grade: int
    level: CustomTypes.GradeLevelEnum


class GradeRelationshipSchema(BaseModel):
    """This model represents the relationships of a GradeSchema.
    It is used to define the relationships between the GradeSchema and other schemas.
    """

    teachers: Optional[List[TeacherSchema]]
