from typing import Annotated

from fastapi import APIRouter, Depends

from api.v1.routers.dependencies import ProtectedRoute
from api.v1.routers.private.schema import AdminInfo, StudentInfo, TeacherInfo
from models.user import User
from schema.models.user_schema import UserSchema
from utils.enum import RoleEnum

router = APIRouter(prefix="/me", tags=["Me"])

allowed_roles = ProtectedRoute([RoleEnum.ADMIN, RoleEnum.TEACHER, RoleEnum.STUDENT])
protected_route = Annotated[User, Depends(allowed_roles)]


@router.get(
    "/",
    response_model=UserSchema,
)
def get_logged_in_user(user_in: protected_route) -> User:
    """
    Returns the current logged in user information.
    """
    return user_in


@router.get(
    "/admin",
    response_model=AdminInfo,
)
def get_admin_basic_info(user_in: protected_route) -> User:
    """
    Returns the current logged in user information.
    """
    print(user_in.created_at, user_in.created_at.tzinfo)
    return user_in


@router.get(
    "/teacher",
    response_model=TeacherInfo,
)
def get_teacher_basic_info(user_in: protected_route) -> User:
    """
    Returns the current logged in user information.
    """
    return user_in


@router.get(
    "/student",
    response_model=StudentInfo,
)
def get_student_basic_info(user_in: protected_route) -> User:
    """
    Returns the current logged in user information.
    """
    return user_in
