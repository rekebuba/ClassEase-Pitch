from typing import TYPE_CHECKING, List
from pydantic import BaseModel

if TYPE_CHECKING:
    from extension.pydantic.models.teacher_schema import TeacherSchema


class SubjectSchema(BaseModel):
    """
    This model represents a subject in the system. It inherits from BaseModel.
    """

    name: str

    # Relationships
    teachers: List[TeacherSchema]
