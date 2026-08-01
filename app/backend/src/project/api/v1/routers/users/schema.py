import uuid

from pydantic import AwareDatetime

from project.api.v1.routers.auth.schema import MembershipSummary, SchoolSummary
from project.schema.models.admin_schema import AdminSchema
from project.schema.models.student_schema import StudentSchema
from project.schema.models.teacher_schema import TeacherSchema
from project.schema.models.user_schema import UserSchema
from project.utils.enum import RoleEnum


class CurrentUserInfo(UserSchema):
    id: uuid.UUID
    username: str
    role: RoleEnum
    image_path: str | None
    created_at: AwareDatetime
    active_school: SchoolSummary
    active_membership: MembershipSummary
    available_memberships: list[MembershipSummary]


class AdminInfo(CurrentUserInfo):
    admin: AdminSchema


class TeacherInfo(CurrentUserInfo):
    teacher: TeacherSchema


class StudentInfo(CurrentUserInfo):
    student: StudentSchema
