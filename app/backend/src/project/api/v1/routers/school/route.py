import uuid

from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from starlette import status

from project.api.v1.routers.dependencies import (
    AuthenticatedRoute,
    SessionDep,
)
from project.api.v1.routers.school.schema import (
    NewSchool,
    NewSchoolMembership,
    SuccessNewSchoolMembership,
    SuccessSchoolResponse,
)
from project.core.access_control import (
    ensure_membership_role,
)
from project.models import (
    Role,
    School,
    SchoolMembership,
)
from project.utils.enum import MfaStateEnum, RoleEnum

router = APIRouter(prefix="/schools", tags=["school"])


@router.post(
    "",
    status_code=201,
    description="Create a new school",
    response_model=SuccessSchoolResponse,
)
async def create_school(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    data: NewSchool,
) -> SuccessSchoolResponse:
    """Create a new school."""
    if (await session.execute(select(School).where(School.slug == data.slug))).scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="School with this slug already exists",
        )

    school = School(
        name=data.name,
        slug=data.slug,
        status=data.status,
        domain=data.domain,
        logo_path=data.logo_path,
        primary_color=data.primary_color,
        settings=data.settings,
    )
    session.add(school)
    await session.commit()

    return SuccessSchoolResponse(message="School created successfully", school_id=school.id)


@router.post(
    "/{school_id}/membership",
    status_code=status.HTTP_201_CREATED,
    description="Setup a school",
    response_model=SuccessNewSchoolMembership,
)
async def assign_school_membership(
    school_id: uuid.UUID,
    session: SessionDep,
    user_in: AuthenticatedRoute,
    new_membership: NewSchoolMembership,
) -> SuccessNewSchoolMembership:
    """Assign a user to a school with a specific role."""
    if not user_in.has_role(RoleEnum.OWNER):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    school = await session.get(School, school_id)
    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="School not found")

    role = (await session.execute(select(Role).where(Role.name == new_membership.role))).scalar_one_or_none()

    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    existing_membership = (
        await session.execute(
            select(SchoolMembership).where(
                SchoolMembership.school_id == school_id,
                SchoolMembership.user_id == new_membership.user_id,
            )
        )
    ).scalar_one_or_none()

    if existing_membership:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this school",
        )

    membership = SchoolMembership(
        school_id=school_id,
        user_id=new_membership.user_id,
        mfa_state=MfaStateEnum.VERIFIED,
    )

    session.add(membership)
    await session.flush()

    await ensure_membership_role(session, membership, role, school.id)

    return SuccessNewSchoolMembership(
        message="Membership assigned successfully",
        school_id=school.id,
        membership_id=membership.id,
        role_id=role.id,
    )
