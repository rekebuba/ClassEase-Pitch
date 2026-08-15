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
    AcademicTerm,
    AssessmentScheme,
    AssessmentSchemeComponent,
    ClassSection,
    Department,
    Grade,
    GradeStream,
    Position,
    School,
    SchoolMembership,
    Section,
    Stream,
    Subject,
    SubjectOffering,
    Year,
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
from tests.utils.type_test import MockLogin, MockSignUp

f = Faker()

PROVISIONED_MODELS = (
    Year,
    AcademicTerm,
    Subject,
    Grade,
    Section,
    Stream,
    GradeStream,
    AssessmentScheme,
    AssessmentSchemeComponent,
    SubjectOffering,
    ClassSection,
    Department,
    Position,
)


async def _assert_provisioned_models_counts(
    *,
    tenant_session: AsyncSession,
    school_id: uuid.UUID | None,
) -> dict[str, int]:
    counts: dict[str, int] = {
        model.__tablename__: await _count_rows(
            tenant_session=tenant_session,
            model=model,
            school_id=school_id,
        )
        for model in PROVISIONED_MODELS
    }

    assert counts["years"] == 1, f"Expected 1 year, got {counts['years']}"
    assert counts["academic_terms"] == 2, f"Expected 2 academic terms, got {counts['academic_terms']}"
    assert counts["subjects"] == 21, f"Expected 21 subjects, got {counts['subjects']}"
    assert counts["grades"] == 12, f"Expected 12 grades, got {counts['grades']}"
    assert counts["sections"] == 36, f"Expected 36 sections, got {counts['sections']}"
    assert counts["streams"] == 2, f"Expected 2 streams, got {counts['streams']}"
    assert counts["grade_streams"] == 14, f"Expected 14 grade streams, got {counts['grade_streams']}"
    assert counts["assessment_schemes"] == 1, f"Expected 1 assessment scheme, got {counts['assessment_schemes']}"
    assert counts["assessment_scheme_components"] == 12, (
        f"Expected 12 assessment scheme components, got {counts['assessment_scheme_components']}"
    )
    assert counts["subject_offerings"] == 130, f"Expected 130 subject offerings, got {counts['subject_offerings']}"
    assert counts["class_sections"] == 36, f"Expected 36 class sections, got {counts['class_sections']}"
    assert counts["departments"] == 7, f"Expected 7 departments, got {counts['departments']}"
    assert counts["positions"] == 19, f"Expected 19 positions, got {counts['positions']}"

    return counts


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
        membership=secondary_membership,
        role_enum=secondary_roles[RoleEnum.TEACHER].name,
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
