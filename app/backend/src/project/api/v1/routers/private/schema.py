from project.api.v1.routers.auth.schema import MembershipSummary, SchoolSummary
from project.schema.models.admin_schema import AdminSchema
from project.schema.models.student_schema import StudentSchema
from project.schema.models.teacher_schema import TeacherSchema
from project.schema.models.user_schema import UserSchema


class CurrentUserInfo(UserSchema):
    active_school: SchoolSummary
    active_membership: MembershipSummary
    available_memberships: list[MembershipSummary]


class AdminInfo(CurrentUserInfo):
    admin: AdminSchema


class TeacherInfo(CurrentUserInfo):
    teacher: TeacherSchema


class StudentInfo(CurrentUserInfo):
    student: StudentSchema
