from schema.models.admin_schema import AdminSchema
from schema.models.student_schema import StudentSchema
from schema.models.teacher_schema import TeacherSchema
from schema.models.user_schema import UserSchema


class AdminInfo(UserSchema):
    admin: AdminSchema


class TeacherInfo(UserSchema):
    teacher: TeacherSchema


class StudentInfo(UserSchema):
    student: StudentSchema
