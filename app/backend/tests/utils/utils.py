import random
import uuid
from datetime import datetime, timezone
from typing import Any, TypeVar
from uuid import uuid4

from faker import Faker
from httpx import AsyncClient
from pydantic import EmailStr, SecretStr
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from project.api.v1.routers.auth.schema import (
    LoginTokenResponse,
    MessageResponse,
    SignUpRequest,
)
from project.api.v1.routers.auth.service import (
    generate_email_verification_token,
)
from project.core.access_control import (
    ensure_membership_role,
    get_or_create_legacy_school,
    provision_user_membership,
    seed_system_roles,
)
from project.core.config import settings
from project.models import (
    School,
    SchoolMembership,
)
from project.models.base.school_mixin import SchoolScopedMixin
from project.schema.schema import SuccessResponse
from project.utils.enum import (
    GenderEnum,
    MfaStateEnum,
    RoleEnum,
    SchoolStatusEnum,
)
from tests.factories.api_data import LoginFactory
from tests.utils.type_test import MockLogin, MockSignUp, SchoolAdmin

f = Faker()


async def _signup_user(client: AsyncClient, user: SignUpRequest) -> MockSignUp:
    r = await client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json=user.model_dump(mode="json"),
    )
    assert r.status_code == 201, f"Expected 201, got {r.status_code}. {r.text}"
    return MockSignUp(request=user, response=SuccessResponse.model_validate(r.json()))


async def _login(
    client: AsyncClient,
    *,
    username: str,
    password: str,
    school_slug: str | None = None,
) -> MockLogin:
    login_form = LoginFactory.create(
        username=username,
        password=password,
        school_slug=school_slug,
    )

    r = await client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": login_form.username,
            "password": login_form.password,
            "schoolSlug": login_form.school_slug,
        },
    )
    assert r.status_code == 200, f"Expected 200, got {r.status_code}. Response: {r.text}"

    response = LoginTokenResponse.model_validate(r.json())
    return MockLogin(
        request=login_form,
        response=response,
        headers={"Authorization": f"Bearer {response.access_token}"},
    )


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

    return {"Authorization": f"Bearer {response.response.access_token}"}


async def moc_verify_email(client: AsyncClient, email: EmailStr) -> None:
    token = generate_email_verification_token(email)

    r = await client.get(f"{settings.API_V1_STR}/auth/verify-email", params={"token": token})

    assert r.status_code == 200

    result = MessageResponse.model_validate_json(r.text)
    assert result.message == "Email successfully verified"


async def _create_multi_school_user(
    db_session: AsyncSession,
    *,
    password: str,
) -> dict[str, Any]:
    primary_school = await get_or_create_legacy_school(system_session=db_session)
    user_key = uuid4().hex[:12]
    login_identifier = f"auth-user-{user_key}"
    email = f"{login_identifier}@example.com"

    user, primary_membership = await provision_user_membership(
        db_session,
        first_name=f.first_name(),
        father_name=f.last_name(),
        grand_father_name=f.last_name(),
        gender=random.choice(list(GenderEnum)),
        date_of_birth=f.date_of_birth(tzinfo=timezone.utc),
        school_id=primary_school.id,
        membership_role_name=RoleEnum.ADMIN,
        login_identifier=login_identifier,
        password=SecretStr(password),
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

    secondary_roles = await seed_system_roles(db_session)
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
        secondary_roles[RoleEnum.TEACHER],
        school_id=secondary_school.id,
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


def find_admin_in_school(
    *,
    admin_membership: list[SchoolAdmin],
    school_id: uuid.UUID,
):
    for school_admin in admin_membership:
        if school_admin.school.response.school_id == school_id:
            for member in school_admin.admins:
                if member.school.response.school_id == school_id:
                    return member
    return None


T = TypeVar("T", bound=SchoolScopedMixin)


async def _count_rows(
    *,
    tenant_session: AsyncSession,
    model: type[T],
    school_id: uuid.UUID | None,
) -> int:
    return (
        await tenant_session.execute(select(func.count()).select_from(model).where(model.school_id == school_id))
    ).scalar_one()
