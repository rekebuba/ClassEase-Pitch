from project.schema.models.admin_schema import AdminSchema
from project.schema.models.student_schema import StudentSchema
from project.schema.models.teacher_schema import TeacherSchema
from project.schema.models.user_schema import UserSchema


class AdminInfo(UserSchema):
    admin: AdminSchema


class TeacherInfo(UserSchema):
    teacher: TeacherSchema


class StudentInfo(UserSchema):
    student: StudentSchema
