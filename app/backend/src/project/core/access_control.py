import hashlib
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable, Optional, Sequence

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
from project.utils.enum import (
    AuthProviderEnum,
    AuthSessionAssuranceEnum,
    MfaStateEnum,
    RoleEnum,
    SchoolMembershipStatusEnum,
    SchoolStatusEnum,
)

DEFAULT_PERMISSION_DESCRIPTIONS: dict[str, str] = {
    "school.manage": "Manage tenant settings and privileged school actions.",
    "years.read": "Read academic years.",
    "years.write": "Create and update academic years.",
    "grades.read": "Read grades.",
    "grades.write": "Create and update grades.",
    "subjects.read": "Read subjects.",
    "subjects.write": "Create and update subjects.",
    "streams.read": "Read streams.",
    "streams.write": "Create and update streams.",
    "sections.read": "Read sections.",
    "sections.write": "Create and update sections.",
    "students.read": "Read students.",
    "students.write": "Create and update students.",
    "employees.read": "Read employees.",
    "employees.write": "Create and update employees.",
    "registrations.create": "Create school registrations.",
    "teachers.assign": "Assign teachers to academic work.",
    "auth.switch_school": "Switch between available memberships.",
    "records.transfer": "Manage record transfer requests.",
}

DEFAULT_ROLE_PERMISSIONS: dict[str, set[str]] = {
    "school_owner": set(DEFAULT_PERMISSION_DESCRIPTIONS.keys()),
    "school_admin": {
        "years.read",
        "years.write",
        "grades.read",
        "grades.write",
        "subjects.read",
        "subjects.write",
        "streams.read",
        "streams.write",
        "sections.read",
        "sections.write",
        "students.read",
        "students.write",
        "employees.read",
        "employees.write",
        "registrations.create",
        "teachers.assign",
        "auth.switch_school",
        "records.transfer",
    },
    "registrar": {
        "years.read",
        "grades.read",
        "subjects.read",
        "streams.read",
        "sections.read",
        "students.read",
        "students.write",
        "employees.read",
        "registrations.create",
        "records.transfer",
    },
    "teacher": {
        "years.read",
        "grades.read",
        "subjects.read",
        "sections.read",
        "students.read",
        "auth.switch_school",
    },
    "student": {
        "years.read",
        "subjects.read",
        "auth.switch_school",
    },
    "parent": {
        "years.read",
        "auth.switch_school",
    },
}

ROLE_PRIORITY: tuple[str, ...] = (
    "school_owner",
    "school_admin",
    "registrar",
    "teacher",
    "student",
    "parent",
)

ROLE_TO_SHELL_ROLE: dict[str, RoleEnum] = {
    "school_owner": RoleEnum.ADMIN,
    "school_admin": RoleEnum.ADMIN,
    "registrar": RoleEnum.ADMIN,
    "teacher": RoleEnum.TEACHER,
    "student": RoleEnum.STUDENT,
    "parent": RoleEnum.PARENT,
}


def hash_refresh_token(refresh_token: str) -> str:
    return hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(48)


def resolve_membership_role_names(membership: SchoolMembership) -> set[str]:
    return {
        membership_role.role.name for membership_role in membership.membership_roles
    }


def resolve_membership_permissions(membership: SchoolMembership) -> set[str]:
    permissions: set[str] = set()
    for membership_role in membership.membership_roles:
        for role_permission in membership_role.role.role_permissions:
            permissions.add(role_permission.permission.code)
    return permissions


def resolve_shell_role_from_names(
    role_names: Iterable[str],
    *,
    fallback: RoleEnum,
) -> RoleEnum:
    role_name_set = set(role_names)
    for role_name in ROLE_PRIORITY:
        if role_name in role_name_set:
            return ROLE_TO_SHELL_ROLE[role_name]
    return fallback


async def get_membership_with_roles(
    session: AsyncSession,
    membership_id: uuid.UUID,
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
        )
    ).scalar_one_or_none()


async def get_school_by_slug(session: AsyncSession, slug: str) -> School | None:
    return (
        await session.execute(select(School).where(School.slug == slug))
    ).scalar_one_or_none()


async def get_or_create_legacy_school(session: AsyncSession) -> School:
    school = await get_school_by_slug(session, settings.LEGACY_SCHOOL_SLUG)
    if school is not None:
        return school

    school = School(
        name=settings.LEGACY_SCHOOL_NAME,
        slug=settings.LEGACY_SCHOOL_SLUG,
        status=SchoolStatusEnum.ACTIVE,
        settings={"bootstrapMode": "legacy"},
    )
    session.add(school)
    await session.flush()
    return school


async def seed_permissions(session: AsyncSession) -> dict[str, Permission]:
    permission_codes = list(DEFAULT_PERMISSION_DESCRIPTIONS.keys())
    existing_permissions = (
        (
            await session.execute(
                select(Permission).where(Permission.code.in_(permission_codes))
            )
        )
        .scalars()
        .all()
    )
    by_code = {permission.code: permission for permission in existing_permissions}

    for code, description in DEFAULT_PERMISSION_DESCRIPTIONS.items():
        if code in by_code:
            continue
        permission = Permission(code=code, description=description)
        session.add(permission)
        await session.flush()
        by_code[code] = permission

    return by_code


async def seed_school_roles(
    session: AsyncSession,
    school: School,
) -> dict[str, Role]:
    """
    makes sure a school has the default system roles
    and that each role has the expected permissions.
    """
    permissions = await seed_permissions(session)
    existing_roles = (
        (
            await session.execute(
                select(Role)
                .where(Role.school_id == school.id)
                .options(
                    selectinload(Role.role_permissions).selectinload(
                        RolePermission.permission
                    )
                )
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
                school_id=school.id,
                name=role_name,
                description=f"System role: {role_name.replace('_', ' ')}",
                is_system=True,
            )
            session.add(role)
            await session.flush()
            roles_by_name[role_name] = role

        existing_permission_codes = {
            role_permission.permission.code for role_permission in role.role_permissions
        }
        for permission_code in permission_codes - existing_permission_codes:
            new_permission = permissions.get(permission_code)
            if new_permission:
                session.add(
                    RolePermission(
                        role_id=role.id,
                        permission_id=new_permission.id,
                    )
                )

    await session.flush()
    return roles_by_name


async def ensure_membership_role(
    session: AsyncSession,
    membership: SchoolMembership,
    role: Role,
) -> None:
    existing = (
        await session.execute(
            select(MembershipRole).where(
                MembershipRole.membership_id == membership.id,
                MembershipRole.role_id == role.id,
            )
        )
    ).scalar_one_or_none()
    if existing is None:
        session.add(MembershipRole(membership_id=membership.id, role_id=role.id))
        membership.permissions_version += 1
        await session.flush()


async def provision_user_membership(
    session: AsyncSession,
    *,
    school: School,
    shell_role: RoleEnum,
    membership_role_name: str,
    login_identifier: Optional[str],
    password: Optional[str],
    email: Optional[str],
    phone: Optional[str],
    is_active: bool,
    is_verified: bool,
    mfa_state: MfaStateEnum,
) -> tuple[User, SchoolMembership]:
    user = User(
        role=shell_role,
        username=login_identifier,
        email=email,
        phone=phone,
        is_active=is_active,
        is_verified=is_verified,
    )
    session.add(user)
    await session.flush()

    if password is not None:
        session.add(
            AuthIdentity(
                user_id=user.id,
                provider=AuthProviderEnum.PASSWORD,
                password=get_password_hash(password),
            )
        )

    membership = SchoolMembership(
        user_id=user.id,
        school_id=school.id,
        status=SchoolMembershipStatusEnum.ACTIVE
        if is_active
        else SchoolMembershipStatusEnum.PENDING,
        login_identifier=login_identifier,
        joined_at=datetime.now(timezone.utc),
        left_at=None,
        mfa_state=mfa_state,
        is_primary=True,
        permissions_version=1,
    )
    session.add(membership)
    await session.flush()

    school_roles = await seed_school_roles(session, school)
    await ensure_membership_role(
        session, membership, school_roles[membership_role_name]
    )
    return user, membership


async def create_auth_session(
    session: AsyncSession,
    *,
    user: User,
    membership: SchoolMembership,
    refresh_token: str,
    user_agent: Optional[str],
    ip_address: Optional[str],
    assurance_level: AuthSessionAssuranceEnum,
) -> AuthSession:
    now = datetime.now(timezone.utc)
    auth_session = AuthSession(
        user_id=user.id,
        school_id=membership.school_id,
        membership_id=membership.id,
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
            membership_id=membership_id,
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
        (SchoolMembership.login_identifier == identifier)
        | (User.email == identifier)
        | (User.username == identifier)
    )
    return (await session.execute(stmt)).scalars().unique().all()


async def load_user_memberships_for_user(
    session: AsyncSession,
    *,
    user_id: uuid.UUID,
    school_slug: str | None = None,
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
    )
    if school_slug is not None:
        stmt = stmt.where(School.slug == school_slug)
    return (await session.execute(stmt)).scalars().unique().all()
