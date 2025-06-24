from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel

from models.base_model import CustomTypes

if TYPE_CHECKING:
    from extension.pydantic.models.user_schema import UserSchema


class StudentSchema(BaseModel):
    """
    This model represents a student in the system. It inherits from BaseModel.
    """

    first_name: str
    father_name: str
    grand_father_name: str
    date_of_birth: str
    gender: CustomTypes.GenderEnum

    father_phone: str
    mother_phone: str
    guardian_name: str
    guardian_phone: str

    start_year_id: str
    current_year_id: str
    current_grade_id: str
    next_grade_id: str | None = None
    semester_id: str | None = None
    has_passed: bool = False

    # Relationships
    user: Optional[UserSchema] = None
