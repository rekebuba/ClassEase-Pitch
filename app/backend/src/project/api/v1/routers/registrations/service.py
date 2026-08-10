import uuid
from datetime import date
from typing import Optional

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from project.core.access_control import ensure_membership_role, seed_system_roles
from project.core.security import get_password_hash
from project.models import (
    AuthIdentity,
    School,
    SchoolMembership,
    User,
    UserGuardian,
)
from project.utils.enum import (
    AuthProviderEnum,
    GenderEnum,
    MfaStateEnum,
    RoleEnum,
    SchoolMembershipStatusEnum,
)


async def find_existing_user(
    session: AsyncSession,
    *,
    email: Optional[str] = None,
    phone: Optional[str] = None,
) -> Optional[User]:
    """
    Finds an existing user by email or phone.
    """
    if not email and not phone:
        return None

    filters = []
    if email:
        filters.append(User.email == email)
    if phone:
        filters.append(User.phone == phone)

    stmt = select(User).where(or_(*filters))
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_or_create_user(
    session: AsyncSession,
    *,
    first_name: str,
    father_name: str,
    grand_father_name: Optional[str],
    gender: GenderEnum,
    date_of_birth: date,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    role: RoleEnum = RoleEnum.STUDENT,
) -> User:
    """
    Gets an existing user or creates a new one with the provided profile information.
    """
    user = await find_existing_user(session, email=email, phone=phone)

    if user:
        # Update profile if it was empty
        if not user.first_name:
            user.first_name = first_name
            user.father_name = father_name
            user.grand_father_name = grand_father_name
            user.gender = gender
            user.date_of_birth = date_of_birth
        return user

    # Create new user
    user = User(
        first_name=first_name,
        father_name=father_name,
        grand_father_name=grand_father_name,
        gender=gender,
        date_of_birth=date_of_birth,
        email=email,
        phone=phone,
        username=username,
        is_active=True,  # Defaulting to active for now, can be adjusted
        is_verified=False,
    )
    session.add(user)
    await session.flush()

    if password:
        auth_identity = AuthIdentity(
            user_id=user.id,
            provider=AuthProviderEnum.PASSWORD,
            password=get_password_hash(password),
        )
        session.add(auth_identity)

    return user


async def ensure_school_membership(
    session: AsyncSession,
    *,
    user: User,
    school: School,
    role_name: RoleEnum,
) -> SchoolMembership:
    """
    Ensures a user has a membership in a school with the specified role.
    """
    stmt = select(SchoolMembership).where(
        SchoolMembership.user_id == user.id,
        SchoolMembership.school_id == school.id,
    )
    result = await session.execute(stmt)
    membership = result.scalar_one_or_none()

    if not membership:
        membership = SchoolMembership(
            user_id=user.id,
            school_id=school.id,
            status=SchoolMembershipStatusEnum.ACTIVE,
            mfa_state=MfaStateEnum.VERIFIED,
            is_primary=True,
            permissions_version=1,
        )
        session.add(membership)
        await session.flush()

    system_roles = await seed_system_roles(session)
    if role_name in system_roles:
        await ensure_membership_role(session, membership, system_roles[role_name], school.id)

    return membership


async def link_parent_to_student(
    session: AsyncSession,
    *,
    guardian_user_id: uuid.UUID,
    dependent_user_id: uuid.UUID,
) -> None:
    """
    Creates a global link between a parent user and a student user.
    """
    stmt = select(UserGuardian).where(
        UserGuardian.guardian_user_id == guardian_user_id,
        UserGuardian.dependent_user_id == dependent_user_id,
    )
    result = await session.execute(stmt)
    existing = result.scalar_one_or_none()

    if not existing:
        link = UserGuardian(
            guardian_user_id=guardian_user_id,
            dependent_user_id=dependent_user_id,
        )
        session.add(link)
        await session.flush()
