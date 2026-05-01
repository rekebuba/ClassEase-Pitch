from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from project.api.v1.routers.auth.schema import MembershipSummary, SchoolSummary
from project.api.v1.routers.dependencies import (
    SessionDep,
    admin_route,
    shared_route,
    student_route,
    teacher_route,
)
from project.api.v1.routers.private.schema import (
    AdminInfo,
    CurrentUserInfo,
    StudentInfo,
    TeacherInfo,
)
from project.core.access_control import (
    load_user_memberships_for_user,
    resolve_membership_permissions,
    resolve_membership_role_names,
    resolve_shell_role_from_names,
)
from project.models import User

router = APIRouter(prefix="/me", tags=["Me"])


@router.get(
    "",
    response_model=CurrentUserInfo,
)
async def get_logged_in_user(session: SessionDep, user_in: shared_route) -> dict:
    """
    Returns the current logged in user information.
    """
    memberships = await load_user_memberships_for_user(session, user_id=user_in.user.id)
    return {
        "id": user_in.user.id,
        "username": user_in.membership.login_identifier or user_in.user.username,
        "role": user_in.shell_role,
        "image_path": user_in.user.image_path,
        "created_at": user_in.user.created_at,
        "active_school": SchoolSummary(
            id=user_in.membership.school.id,
            name=user_in.membership.school.name,
            slug=user_in.membership.school.slug,
            status=user_in.membership.school.status,
        ),
        "active_membership": MembershipSummary(
            id=user_in.membership.id,
            school_id=user_in.membership.school_id,
            school_slug=user_in.membership.school.slug,
            school_name=user_in.membership.school.name,
            status=user_in.membership.status,
            login_identifier=user_in.membership.login_identifier,
            is_primary=user_in.membership.is_primary,
            role_names=sorted(resolve_membership_role_names(user_in.membership)),
            shell_role=user_in.shell_role,
            permissions=sorted(resolve_membership_permissions(user_in.membership)),
        ),
        "available_memberships": [
            MembershipSummary(
                id=membership.id,
                school_id=membership.school_id,
                school_slug=membership.school.slug,
                school_name=membership.school.name,
                status=membership.status,
                login_identifier=membership.login_identifier,
                is_primary=membership.is_primary,
                role_names=sorted(resolve_membership_role_names(membership)),
                shell_role=resolve_shell_role_from_names(
                    resolve_membership_role_names(membership),
                    fallback=membership.user.role,
                ),
                permissions=sorted(resolve_membership_permissions(membership)),
            )
            for membership in memberships
        ],
    }


@router.get(
    "/admin",
    response_model=AdminInfo,
)
async def get_admin_basic_info(session: SessionDep, user_in: admin_route) -> dict:
    """
    Returns the current logged in user information.
    """
    payload = await get_logged_in_user(session, user_in)
    user = (
        await session.execute(
            select(User)
            .where(User.id == user_in.user.id)
            .options(selectinload(User.admin_profiles))
        )
    ).scalar_one()

    payload["admin"] = user.admin
    return payload


@router.get(
    "/teacher",
    response_model=TeacherInfo,
)
async def get_teacher_basic_info(session: SessionDep, user_in: teacher_route) -> dict:
    """
    Returns the current logged in user information.
    """
    payload = await get_logged_in_user(session, user_in)
    user = (
        await session.execute(
            select(User)
            .where(User.id == user_in.user.id)
            .options(selectinload(User.employee_profiles))
        )
    ).scalar_one()
    payload["teacher"] = user.teacher
    return payload


@router.get(
    "/student",
    response_model=StudentInfo,
)
async def get_student_basic_info(session: SessionDep, user_in: student_route) -> dict:
    """
    Returns the current logged in user information.
    """
    payload = await get_logged_in_user(session, user_in)
    user = (
        await session.execute(
            select(User)
            .where(User.id == user_in.user.id)
            .options(selectinload(User.student_profiles))
        )
    ).scalar_one()
    payload["student"] = user.student
    return payload
