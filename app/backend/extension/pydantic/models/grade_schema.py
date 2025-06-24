from typing import TYPE_CHECKING, List, Optional
from pydantic import BaseModel

from models.base_model import CustomTypes

if TYPE_CHECKING:
    from extension.pydantic.models.teacher_schema import TeacherSchema


class GradeSchema(BaseModel):
    """
    This model represents a grade in the system. It inherits from BaseModel.
    """

    grade: int
    level: CustomTypes.GradeLevelEnum

    # Relationships
    teachers: Optional[List[TeacherSchema]]
