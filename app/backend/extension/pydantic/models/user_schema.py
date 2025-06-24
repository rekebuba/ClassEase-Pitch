from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel, ConfigDict

from models.base_model import CustomTypes

if TYPE_CHECKING:
    from .admin_schema import AdminSchema
    from .teacher_schema import TeacherSchema
    from .student_schema import StudentSchema


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    identification: str
    password: str
    role: CustomTypes.RoleEnum
    image_path: Optional[str] = None
    national_id: str

    # Relationships
    admins: Optional[AdminSchema] = None
    teachers: Optional[TeacherSchema] = None
    students: Optional[StudentSchema] = None
