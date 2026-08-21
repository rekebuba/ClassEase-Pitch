import hashlib
import secrets
import uuid
from datetime import date, datetime, timedelta, timezone
from typing import Any, Iterable, Optional, Sequence

from fastapi import HTTPException, status
from pydantic import SecretStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from project.core.config import settings
from project.core.security import get_password_hash
from project.models import (
    AuditLog,
    AuthIdentity,
    AuthSession,
    MembershipRole,
    Permission,
    Role,
    RolePermission,
    School,
    SchoolMembership,
    User,
)
from project.services.school_provisioning import SchoolProvisioningService
from project.utils.enum import (
    AuthProviderEnum,
    AuthSessionAssuranceEnum,
    GenderEnum,
    MfaStateEnum,
    PermissionEnum,
    RoleEnum,
    SchoolMembershipStatusEnum,
    SchoolStatusEnum,
)

DEFAULT_PERMISSION_DESCRIPTIONS: dict[PermissionEnum, str] = {
    PermissionEnum.SCHOOLS_READ: "Read school information.",
    PermissionEnum.SCHOOLS_MANAGE: "Manage tenant settings and privileged school actions.",
    PermissionEnum.YEARS_READ: "Read academic years.",
    PermissionEnum.YEARS_WRITE: "Create and update academic years.",
    PermissionEnum.GRADES_READ: "Read grades.",
    PermissionEnum.GRADES_WRITE: "Create and update grades.",
    PermissionEnum.SUBJECTS_READ: "Read subjects.",
    PermissionEnum.SUBJECTS_WRITE: "Create and update subjects.",
    PermissionEnum.STREAMS_READ: "Read streams.",
    PermissionEnum.STREAMS_WRITE: "Create and update streams.",
    PermissionEnum.SECTIONS_READ: "Read sections.",
    PermissionEnum.SECTIONS_WRITE: "Create and update sections.",
    PermissionEnum.STUDENTS_READ: "Read students.",
    PermissionEnum.STUDENTS_WRITE: "Create and update students.",
    PermissionEnum.EMPLOYEES_READ: "Read employees.",
    PermissionEnum.EMPLOYEES_WRITE: "Create and update employees.",
    PermissionEnum.REGISTRATIONS_CREATE: "Create school registrations.",
    PermissionEnum.TEACHERS_ASSIGN: "Assign teachers to academic work.",
    PermissionEnum.AUTH_SWITCH_SCHOOL: "Switch between available memberships.",
    PermissionEnum.RECORDS_TRANSFER: "Manage record transfer requests.",
}

DEFAULT_ROLE_PERMISSIONS: dict[RoleEnum, set[PermissionEnum]] = {
    RoleEnum.OWNER: set(DEFAULT_PERMISSION_DESCRIPTIONS.keys()),
    RoleEnum.ADMIN: {
        PermissionEnum.SCHOOLS_READ,
        PermissionEnum.YEARS_READ,
        PermissionEnum.YEARS_WRITE,
        PermissionEnum.GRADES_READ,
        PermissionEnum.GRADES_WRITE,
        PermissionEnum.SUBJECTS_READ,
        PermissionEnum.SUBJECTS_WRITE,
        PermissionEnum.STREAMS_READ,
        PermissionEnum.STREAMS_WRITE,
        PermissionEnum.SECTIONS_READ,
        PermissionEnum.SECTIONS_WRITE,
        PermissionEnum.STUDENTS_READ,
        PermissionEnum.STUDENTS_WRITE,
        PermissionEnum.EMPLOYEES_READ,
        PermissionEnum.EMPLOYEES_WRITE,
        PermissionEnum.REGISTRATIONS_CREATE,
        PermissionEnum.TEACHERS_ASSIGN,
        PermissionEnum.AUTH_SWITCH_SCHOOL,
        PermissionEnum.RECORDS_TRANSFER,
    },
    RoleEnum.REGISTRAR: {
        PermissionEnum.SCHOOLS_READ,
        PermissionEnum.YEARS_READ,
        PermissionEnum.GRADES_READ,
        PermissionEnum.SUBJECTS_READ,
        PermissionEnum.STREAMS_READ,
        PermissionEnum.SECTIONS_READ,
        PermissionEnum.STUDENTS_READ,
        PermissionEnum.STUDENTS_WRITE,
        PermissionEnum.EMPLOYEES_READ,
        PermissionEnum.REGISTRATIONS_CREATE,
        PermissionEnum.RECORDS_TRANSFER,
    },
    RoleEnum.TEACHER: {
        PermissionEnum.SCHOOLS_READ,
        PermissionEnum.YEARS_READ,
        PermissionEnum.GRADES_READ,
        PermissionEnum.SUBJECTS_READ,
        PermissionEnum.SECTIONS_READ,
        PermissionEnum.STUDENTS_READ,
        PermissionEnum.AUTH_SWITCH_SCHOOL,
    },
    RoleEnum.EMPLOYEE: {
        PermissionEnum.SCHOOLS_READ,
        PermissionEnum.YEARS_READ,
        PermissionEnum.SUBJECTS_READ,
        PermissionEnum.AUTH_SWITCH_SCHOOL,
    },
    RoleEnum.STUDENT: {
        PermissionEnum.SCHOOLS_READ,
        PermissionEnum.YEARS_READ,
        PermissionEnum.SUBJECTS_READ,
        PermissionEnum.AUTH_SWITCH_SCHOOL,
    },
    RoleEnum.PARENT: {
        PermissionEnum.SCHOOLS_READ,
        PermissionEnum.YEARS_READ,
        PermissionEnum.AUTH_SWITCH_SCHOOL,
    },
    RoleEnum.GUEST: {
        PermissionEnum.SCHOOLS_READ,
        PermissionEnum.AUTH_SWITCH_SCHOOL,
    },
}

PRIVILEGED_MEMBERSHIP_ROLES: set[RoleEnum] = {
    RoleEnum.OWNER,
    RoleEnum.ADMIN,
    RoleEnum.REGISTRAR,
    RoleEnum.TEACHER,
}

ROLE_PRIORITY: tuple[RoleEnum, ...] = (
    RoleEnum.OWNER,
    RoleEnum.ADMIN,
    RoleEnum.REGISTRAR,
    RoleEnum.TEACHER,
    RoleEnum.EMPLOYEE,
    RoleEnum.STUDENT,
    RoleEnum.PARENT,
    RoleEnum.GUEST,
)


def hash_refresh_token(refresh_token: str) -> str:
    return hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(48)


def resolve_membership_role_names(membership: SchoolMembership) -> set[RoleEnum]:
    return {membership_role.role.name for membership_role in membership.membership_roles}


def resolve_membership_permissions(membership: SchoolMembership) -> set[PermissionEnum]:
    permissions: set[PermissionEnum] = set()
    for membership_role in membership.membership_roles:
        for role_permission in membership_role.role.role_permissions:
            permissions.add(role_permission.permission.code)
    return permissions


def resolve_shell_role_from_names(
    role_names: Iterable[RoleEnum],
) -> RoleEnum | None:
    role_name_set = set(role_names)
    for role_name in ROLE_PRIORITY:
        if role_name in role_name_set:
            return role_name
    return None


async def get_membership_with_roles(
    session: AsyncSession,
    membership_id: uuid.UUID,
    skip_school_scope: bool = False,
) -> SchoolMembership | None:
    return (
        await session.execute(
            select(SchoolMembership)
            .where(SchoolMembership.id == membership_id)
            .options(
                selectinload(SchoolMembership.user),
                selectinload(SchoolMembership.school),
                selectinload(SchoolMembership.membership_roles)
                .selectinload(MembershipRole.role)
                .selectinload(Role.role_permissions)
                .selectinload(RolePermission.permission),
            )
            .execution_options(skip_school_scope=skip_school_scope)
        )
    ).scalar_one_or_none()


async def get_school_by_id(
    session: AsyncSession,
    id: uuid.UUID,
) -> School | None:
    return (await session.execute(select(School).where(School.id == id))).scalar_one_or_none()


async def get_or_create_legacy_school(
    *,
    system_session: AsyncSession,
) -> School:
    school = await get_school_by_id(system_session, id=settings.SYSTEM_SCHOOL_ID)

    if not school:
        school = School(
            name=settings.SYSTEM_SCHOOL_NAME,
            slug=settings.SYSTEM_SCHOOL_SLUG,
            status=SchoolStatusEnum.ACTIVE,
            settings={"bootstrapMode": "legacy"},
        )
        school.id = settings.SYSTEM_SCHOOL_ID
        system_session.add(school)
        await system_session.flush()

    existing_year_id = await SchoolProvisioningService._get_blueprint_year_id(
        system_session=system_session, required=False
    )

    if existing_year_id is None:
        await SchoolProvisioningService.ensure_default_blueprint(system_session=system_session)

    return school


async def seed_permissions(session: AsyncSession) -> dict[str, Permission]:
    permission_codes = list(DEFAULT_PERMISSION_DESCRIPTIONS.keys())
    existing_permissions = (
        (await session.execute(select(Permission).where(Permission.code.in_(permission_codes)))).scalars().all()
    )
    by_code = {permission.code: permission for permission in existing_permissions}

    for code, description in DEFAULT_PERMISSION_DESCRIPTIONS.items():
        if code in by_code:
            continue
        permission = Permission(code=code.value, description=description)
        session.add(permission)
        await session.flush()
        by_code[code] = permission

    return by_code


async def seed_system_roles(
    system_session: AsyncSession,
) -> dict[RoleEnum, Role]:
    """
    Ensures system roles exist globally and are correctly mapped to permissions.
    """

    permissions = await seed_permissions(system_session)

    existing_roles = (
        (
            await system_session.execute(
                select(Role)
                .options(selectinload(Role.role_permissions).selectinload(RolePermission.permission))
                .execution_options(populate_existing=True)
            )
        )
        .scalars()
        .all()
    )

    roles_by_name = {role.name: role for role in existing_roles}

    for role_name, permission_codes in DEFAULT_ROLE_PERMISSIONS.items():
        role = roles_by_name.get(role_name)

        if role is None:
            role = Role(
                name=role_name,
                description=f"System role: {role_name.replace('_', ' ')}",
                is_system=True,
            )
            system_session.add(role)
            await system_session.flush()
            roles_by_name[role_name] = role

        existing_permission_codes = {rp.permission.code for rp in role.role_permissions}

        for permission_code in permission_codes - existing_permission_codes:
            new_permission = permissions.get(permission_code)

            if new_permission:
                system_session.add(
                    RolePermission(
                        role_id=role.id,
                        permission_id=new_permission.id,
                    )
                )

    await system_session.flush()
    return roles_by_name


async def ensure_membership_role(
    session: AsyncSession,
    *,
    membership: SchoolMembership,
    role_enum: RoleEnum,
    school_id: uuid.UUID,
) -> None:
    """
    Ensures a MembershipRole exists for the given membership and role.
    """
    role = await session.scalar(select(Role).where(Role.name == role_enum))
    if not role:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Role '{role_enum.value}' not found.",
        )

    existing = (
        await session.execute(
            select(MembershipRole).where(
                MembershipRole.membership_id == membership.id,
                MembershipRole.role_id == role.id,
                MembershipRole.school_id == school_id,
            )
        )
    ).scalar_one_or_none()
    if existing is None:
        membership_role = MembershipRole(
            school_id=school_id,
            membership_id=membership.id,
            role_id=role.id,
        )
        session.add(membership_role)
        membership.permissions_version += 1
        await session.flush()


async def ensure_user_membership_and_role(
    session: AsyncSession,
    user_id: uuid.UUID,
    school_id: uuid.UUID,
    role_enum: RoleEnum,
    mfa_state: MfaStateEnum,
) -> SchoolMembership:
    """Ensures a SchoolMembership exists for a user and assigns the given role."""
    membership = await session.scalar(
        select(SchoolMembership).where(
            SchoolMembership.user_id == user_id,
            SchoolMembership.school_id == school_id,
        )
    )

    if not membership:
        membership = SchoolMembership(
            user_id=user_id,
            school_id=school_id,
            status=SchoolMembershipStatusEnum.ACTIVE,
            mfa_state=mfa_state,
            is_primary=True,
            permissions_version=1,
        )
        session.add(membership)
        await session.flush()

    await ensure_membership_role(
        session,
        membership=membership,
        role_enum=role_enum,
        school_id=school_id,
    )
    return membership


async def provision_user_membership(
    session: AsyncSession,
    *,
    first_name: str,
    father_name: str,
    grand_father_name: Optional[str],
    gender: GenderEnum,
    date_of_birth: date,
    school_id: uuid.UUID,
    membership_role_name: RoleEnum,
    login_identifier: Optional[str],
    password: Optional[SecretStr],
    email: Optional[str],
    phone: Optional[str],
    is_active: bool,
    is_verified: bool,
    mfa_state: MfaStateEnum,
) -> tuple[User, SchoolMembership]:
    # TODO: Check if a User already Exists
    user = User(
        username=login_identifier,
        first_name=first_name,
        father_name=father_name,
        grand_father_name=grand_father_name,
        gender=gender,
        date_of_birth=date_of_birth,
        email=email,
        phone=phone,
        is_active=is_active,
        is_verified=is_verified,
    )
    session.add(user)
    await session.flush()

    if password is not None:
        user.auth_identities.append(
            AuthIdentity(
                user_id=user.id,
                provider=AuthProviderEnum.PASSWORD,
                password=get_password_hash(password),
            )
        )

    membership = SchoolMembership(
        user_id=user.id,
        school_id=school_id,
        status=SchoolMembershipStatusEnum.ACTIVE if is_active else SchoolMembershipStatusEnum.PENDING,
        login_identifier=login_identifier,
        joined_at=datetime.now(timezone.utc),
        left_at=None,
        mfa_state=mfa_state,
        is_primary=True,
        permissions_version=1,
    )
    session.add(membership)
    await session.flush()

    system_roles = await seed_system_roles(session)
    await ensure_membership_role(
        session,
        membership=membership,
        role_enum=system_roles[membership_role_name].name,
        school_id=school_id,
    )
    return user, membership


async def create_auth_session(
    session: AsyncSession,
    *,
    user: User,
    membership: SchoolMembership | None = None,
    refresh_token: str,
    user_agent: Optional[str],
    ip_address: Optional[str],
    assurance_level: AuthSessionAssuranceEnum,
) -> AuthSession:
    now = datetime.now(timezone.utc)
    auth_session = AuthSession(
        user_id=user.id,
        refresh_token_hash=hash_refresh_token(refresh_token),
        user_agent=user_agent,
        ip_address=ip_address,
        assurance_level=assurance_level,
        expires_at=now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        last_seen_at=now,
        revoked_at=None,
        revoke_reason=None,
    )
    session.add(auth_session)
    await session.flush()
    return auth_session


async def get_user_with_auth_context(
    session: AsyncSession,
    *,
    identifier: str,
) -> User | None:
    return (
        await session.execute(
            select(User)
            .where((User.email == identifier) | (User.username == identifier))
            .options(
                selectinload(User.auth_identities),
                selectinload(User.memberships),
            )
        )
    ).scalar_one_or_none()


async def record_audit_log(
    session: AsyncSession,
    *,
    action: str,
    outcome: str,
    school_id: uuid.UUID | None = None,
    user_id: uuid.UUID | None = None,
    membership_id: uuid.UUID | None = None,
    auth_session_id: uuid.UUID | None = None,
    resource_type: str | None = None,
    resource_id: str | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
    details: dict[str, Any] | None = None,
) -> None:
    session.add(
        AuditLog(
            school_id=school_id,
            user_id=user_id,
            auth_session_id=auth_session_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            outcome=outcome,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details or {},
        )
    )
    await session.flush()


async def load_user_memberships_by_identifier(
    session: AsyncSession,
    *,
    identifier: str,
    school_slug: str | None = None,
) -> Sequence[SchoolMembership]:
    stmt = (
        select(SchoolMembership)
        .join(User, User.id == SchoolMembership.user_id)
        .join(School, School.id == SchoolMembership.school_id)
        .where(SchoolMembership.status == SchoolMembershipStatusEnum.ACTIVE)
        .options(
            selectinload(SchoolMembership.school),
            selectinload(SchoolMembership.user).selectinload(User.auth_identities),
            selectinload(SchoolMembership.membership_roles)
            .selectinload(MembershipRole.role)
            .selectinload(Role.role_permissions)
            .selectinload(RolePermission.permission),
        )
    )
    if school_slug is not None:
        stmt = stmt.where(School.slug == school_slug)

    stmt = stmt.where(
        (SchoolMembership.login_identifier == identifier) | (User.email == identifier) | (User.username == identifier)
    )
    return (await session.execute(stmt)).scalars().unique().all()


async def load_user_memberships_for_user(
    session: AsyncSession,
    *,
    user_id: uuid.UUID,
    school_slug: str | None = None,
    skip_school_scope: bool = False,
) -> Sequence[SchoolMembership]:
    stmt = (
        select(SchoolMembership)
        .join(School, School.id == SchoolMembership.school_id)
        .where(
            SchoolMembership.user_id == user_id,
            SchoolMembership.status == SchoolMembershipStatusEnum.ACTIVE,
        )
        .options(
            selectinload(SchoolMembership.school),
            selectinload(SchoolMembership.user).selectinload(User.auth_identities),
            selectinload(SchoolMembership.membership_roles)
            .selectinload(MembershipRole.role)
            .selectinload(Role.role_permissions)
            .selectinload(RolePermission.permission),
        )
        .execution_options(skip_school_scope=skip_school_scope)
    )
    if school_slug is not None:
        stmt = stmt.where(School.slug == school_slug)
    return (await session.execute(stmt)).scalars().unique().all()
