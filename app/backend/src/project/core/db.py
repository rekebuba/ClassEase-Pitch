from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import selectinload

from project.core.access_control import (
    ensure_membership_role,
    get_or_create_legacy_school,
    provision_user_membership,
    seed_school_roles,
)
from project.core.config import settings
from project.core.security import get_password_hash
from project.models import AuthIdentity, SchoolMembership
from project.models.admin import Admin
from project.models.user import User
from project.utils.enum import (
    AuthProviderEnum,
    MfaStateEnum,
    RoleEnum,
    SchoolMembershipStatusEnum,
)

# Create the engine
engine = create_async_engine(
    str(settings.SQLALCHEMY_POSTGRES_DATABASE_URI), future=True
)


async def init_db(session: AsyncSession) -> None:
    """Initialize the database with the first super user and legacy school."""
    school = await get_or_create_legacy_school(session)
    school_roles = await seed_school_roles(session, school)

    user = (
        await session.execute(
            select(User)
            .where(User.username == settings.FIRST_SUPERUSER)
            .options(
                selectinload(User.admin_profiles),
            )
        )
    ).scalar_one_or_none()

    if user is None:
        user, membership = await provision_user_membership(
            session,
            school=school,
            shell_role=RoleEnum.ADMIN,
            membership_role_name="school_owner",
            login_identifier=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD.get_secret_value(),
            email=str(settings.FIRST_SUPERUSER_EMAIL),
            phone=str(settings.FIRST_SUPERUSER_PHONE),
            is_active=True,
            is_verified=True,
            mfa_state=MfaStateEnum.VERIFIED,
        )

        admin = Admin(
            user_id=user.id,
            school_membership_id=membership.id,
            first_name=settings.FIRST_SUPERUSER_NAME,
            father_name=settings.FIRST_SUPERUSER_FATHER_NAME,
            grand_father_name=settings.FIRST_SUPERUSER_GRAND_FATHER_NAME,
            date_of_birth=settings.FIRST_SUPERUSER_DATE_OF_BIRTH,
            gender=settings.FIRST_SUPERUSER_GENDER,
        )
        admin.school_id = school.id
        session.add(admin)
        await session.commit()
        return

    membership = (
        await session.execute(
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
        session.add(membership)
        await session.flush()

    await ensure_membership_role(session, membership, school_roles["school_owner"])

    identity = (
        await session.execute(
            select(AuthIdentity).filter_by(
                user_id=user.id,
                provider=AuthProviderEnum.PASSWORD,
            )
        )
    ).scalar_one_or_none()
    if identity is None:
        session.add(
            AuthIdentity(
                user_id=user.id,
                provider=AuthProviderEnum.PASSWORD,
                password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            )
        )

    admin = user.admin_profiles[0] if user.admin_profiles else None
    if admin is None:
        admin = Admin(
            user_id=user.id,
            school_membership_id=membership.id,
            first_name=settings.FIRST_SUPERUSER_NAME,
            father_name=settings.FIRST_SUPERUSER_FATHER_NAME,
            grand_father_name=settings.FIRST_SUPERUSER_GRAND_FATHER_NAME,
            date_of_birth=settings.FIRST_SUPERUSER_DATE_OF_BIRTH,
            gender=settings.FIRST_SUPERUSER_GENDER,
        )
        session.add(admin)

    admin.school_id = school.id
    admin.school_membership_id = membership.id

    await session.commit()
