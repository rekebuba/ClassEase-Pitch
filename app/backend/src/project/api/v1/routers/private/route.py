
from fastapi import APIRouter

from project.api.v1.routers.dependencies import (
    admin_route,
    shared_route,
    student_route,
    teacher_route,
)
from project.api.v1.routers.private.schema import AdminInfo, StudentInfo, TeacherInfo
from project.models.user import User
from project.schema.models.user_schema import UserSchema

router = APIRouter(prefix="/me", tags=["Me"])


@router.get(
    "/",
    response_model=UserSchema,
)
def get_logged_in_user(user_in: shared_route) -> User:
    """
    Returns the current logged in user information.
    """
    return user_in


@router.get(
    "/admin",
    response_model=AdminInfo,
)
def get_admin_basic_info(user_in: admin_route) -> User:
    """
    Returns the current logged in user information.
    """
    return user_in


@router.get(
    "/teacher",
    response_model=TeacherInfo,
)
def get_teacher_basic_info(user_in: teacher_route) -> User:
    """
    Returns the current logged in user information.
    """
    return user_in


@router.get(
    "/student",
    response_model=StudentInfo,
)
def get_student_basic_info(user_in: student_route) -> User:
    """
    Returns the current logged in user information.
    """
    return user_in
