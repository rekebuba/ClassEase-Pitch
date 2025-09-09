from extension.pydantic.models.admin_schema import AdminSchema
from extension.pydantic.models.student_schema import StudentSchema
from extension.pydantic.models.teacher_schema import TeacherSchema
from extension.pydantic.models.user_schema import UserSchema


class AdminInfo(UserSchema):
    admin: AdminSchema


class TeacherInfo(UserSchema):
    teacher: TeacherSchema


class StudentInfo(UserSchema):
    student: StudentSchema
