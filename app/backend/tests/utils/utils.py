from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from httpx import AsyncClient
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from project.api.v1.routers.auth.schema import (
    LoginTokenResponse,
    MessageResponse,
)
from project.api.v1.routers.auth.service import (
    generate_email_verification_token,
)
from project.core.access_control import (
    ensure_membership_role,
    get_or_create_legacy_school,
    provision_user_membership,
    seed_school_roles,
)
from project.core.config import settings
from project.models import (
    School,
    SchoolMembership,
)
from project.utils.enum import (
    MfaStateEnum,
    RoleEnum,
    SchoolStatusEnum,
)


async def _login(
    client: AsyncClient,
    *,
    username: str,
    password: str,
    school_slug: str | None = None,
) -> LoginTokenResponse:
    login_data: dict[str, str] = {
        "username": username,
        "password": password,
    }
    if school_slug is not None:
        login_data["schoolSlug"] = school_slug

    response = await client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert response.status_code == 200
    return LoginTokenResponse.model_validate_json(response.text)


async def _login_headers(
    client: AsyncClient,
    *,
    username: str,
    password: str,
    school_slug: str | None = None,
) -> dict[str, str]:
    response = await _login(
        client,
        username=username,
        password=password,
        school_slug=school_slug,
    )

    return {"Authorization": f"Bearer {response.access_token}"}


async def moc_verify_email(client: AsyncClient, email: EmailStr) -> None:
    token = generate_email_verification_token(email)

    r = await client.get(
        f"{settings.API_V1_STR}/auth/verify-email", params={"token": token}
    )

    assert r.status_code == 200

    result = MessageResponse.model_validate_json(r.text)
    assert result.message == "Email successfully verified"


async def _create_multi_school_user(
    db_session: AsyncSession,
    *,
    password: str,
) -> dict[str, Any]:
    primary_school = await get_or_create_legacy_school(db_session)
    user_key = uuid4().hex[:12]
    login_identifier = f"auth-user-{user_key}"
    email = f"{login_identifier}@example.com"

    user, primary_membership = await provision_user_membership(
        db_session,
        school=primary_school,
        shell_role=RoleEnum.ADMIN,
        membership_role_name="school_admin",
        login_identifier=login_identifier,
        password=password,
        email=email,
        phone="+251912345678",
        is_active=True,
        is_verified=True,
        mfa_state=MfaStateEnum.VERIFIED,
    )

    secondary_school_slug = f"school-{uuid4().hex[:8]}"
    secondary_school = School(
        name=f"School {secondary_school_slug}",
        slug=secondary_school_slug,
        status=SchoolStatusEnum.ACTIVE,
        settings={},
    )
    db_session.add(secondary_school)
    await db_session.flush()

    secondary_roles = await seed_school_roles(db_session, secondary_school)
    secondary_membership = SchoolMembership(
        user_id=user.id,
        school_id=secondary_school.id,
        status=primary_membership.status,
        login_identifier=login_identifier,
        joined_at=datetime.now(timezone.utc),
        left_at=None,
        mfa_state=MfaStateEnum.VERIFIED,
        is_primary=False,
        permissions_version=1,
    )
    db_session.add(secondary_membership)
    await db_session.flush()

    await ensure_membership_role(
        db_session,
        secondary_membership,
        secondary_roles["teacher"],
    )
    await db_session.commit()

    return {
        "username": login_identifier,
        "email": email,
        "password": password,
        "primary_school_slug": primary_school.slug,
        "primary_membership_id": str(primary_membership.id),
        "secondary_school_slug": secondary_school.slug,
        "secondary_membership_id": str(secondary_membership.id),
    }
