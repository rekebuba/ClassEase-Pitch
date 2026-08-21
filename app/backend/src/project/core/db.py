from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import selectinload

from project.core.access_control import (
    ensure_membership_role,
    get_or_create_legacy_school,
    provision_user_membership,
    seed_system_roles,
)
from project.core.config import settings
from project.core.security import get_password_hash
from project.models import AuthIdentity, SchoolMembership
from project.models.user import User
from project.utils.enum import (
    AuthProviderEnum,
    MfaStateEnum,
    RoleEnum,
    SchoolMembershipStatusEnum,
)

# Create the engine
tenant_engine = create_async_engine(str(settings.SQLALCHEMY_POSTGRES_DATABASE_URI), future=True)
system_engine = create_async_engine(
    str(settings.SQLALCHEMY_POSTGRES_DATABASE_SYSTEM_URI),
    future=True,
)


async def init_db(*, system_session: AsyncSession) -> None:
    """Initialize the database with the first super user and legacy school."""
    school = await get_or_create_legacy_school(system_session=system_session)
    system_roles = await seed_system_roles(system_session)

    user = (
        await system_session.execute(
            select(User).where(User.username == settings.FIRST_SUPERUSER).options(selectinload(User.primary_membership))
        )
    ).scalar_one_or_none()

    if user is None:
        user, membership = await provision_user_membership(
            system_session,
            first_name=settings.FIRST_SUPERUSER_NAME,
            father_name=settings.FIRST_SUPERUSER_FATHER_NAME,
            grand_father_name=settings.FIRST_SUPERUSER_GRAND_FATHER_NAME,
            date_of_birth=settings.FIRST_SUPERUSER_DATE_OF_BIRTH,
            gender=settings.FIRST_SUPERUSER_GENDER,
            school_id=school.id,
            membership_role_name=RoleEnum.OWNER,
            login_identifier=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            email=str(settings.FIRST_SUPERUSER_EMAIL),
            phone=str(settings.FIRST_SUPERUSER_PHONE),
            is_active=True,
            is_verified=True,
            mfa_state=MfaStateEnum.VERIFIED,
        )

    await system_session.flush()

    membership = (
        await system_session.execute(
            select(SchoolMembership).where(
                SchoolMembership.user_id == user.id,
                SchoolMembership.school_id == school.id,
            )
        )
    ).scalar_one_or_none()
    if membership is None:
        membership = SchoolMembership(
            user_id=user.id,
            school_id=school.id,
            status=SchoolMembershipStatusEnum.ACTIVE,
            login_identifier=user.username,
            joined_at=user.created_at,
            left_at=None,
            mfa_state=MfaStateEnum.VERIFIED,
            is_primary=True,
            permissions_version=1,
        )
        system_session.add(membership)
        await system_session.flush()

    await ensure_membership_role(
        system_session,
        membership=membership,
        role_enum=system_roles[RoleEnum.OWNER].name,
        school_id=school.id,
    )

    identity = (
        await system_session.execute(
            select(AuthIdentity).filter_by(
                user_id=user.id,
                provider=AuthProviderEnum.PASSWORD,
            )
        )
    ).scalar_one_or_none()
    if identity is None:
        system_session.add(
            AuthIdentity(
                user_id=user.id,
                provider=AuthProviderEnum.PASSWORD,
                password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            )
        )

    await system_session.commit()
