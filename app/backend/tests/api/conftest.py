import random
from collections.abc import AsyncGenerator
from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from project.api.v1.routers.dependencies import get_db, get_redis
from project.api.v1.routers.registrations.schema import RegistrationResponse
from project.api.v1.routers.year.schema import NewYearSuccess
from project.core.access_control import (
    get_or_create_legacy_school,
    provision_user_membership,
)
from project.core.config import settings
from project.core.db import engine, init_db
from project.main import app
from project.models import Parent, Student
from project.models.base.base_model import Base
from project.schema.models import (
    GradeWithRelatedSchema,
    SectionSchema,
    SectionWithRelatedSchema,
    StreamSchema,
    YearSchema,
    YearWithRelatedSchema,
)
from project.schema.models.stream_schema import StreamWithRelatedSchema
from project.utils.enum import BloodTypeEnum, GenderEnum, MfaStateEnum, RoleEnum
from tests.factories.api_data import NewYearFactory, ParentRegistrationFactory
from tests.utils.utils import _login_headers


@pytest_asyncio.fixture(scope="session", loop_scope="session", autouse=True)
async def db() -> AsyncGenerator[None, None]:
    """Create tables once at the start and drop them at the end."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed data that all tests need
    async with async_sessionmaker(engine, class_=AsyncSession)() as session:
        await init_db(session)

    yield

    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)

    # await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a fresh, transactional session for every single test"""

    async with engine.connect() as conn:
        """Start a transaction, yield a session, and rollback after the test."""
        trans = await conn.begin()

        async_session = async_sessionmaker(
            bind=conn,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        async with async_session() as session:
            yield session

        await trans.rollback()


@pytest_asyncio.fixture(scope="session")
async def test_redis():
    redis_client = Redis.from_url(str(settings.REDIS_URL), decode_responses=True)
    yield redis_client
    await redis_client.aclose()


@pytest_asyncio.fixture(scope="session")
async def client(db_session: AsyncSession, test_redis: Redis):
    """Setup client with dependency overrides."""

    app.dependency_overrides[get_db] = lambda: db_session
    app.dependency_overrides[get_redis] = lambda: test_redis

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
async def admin_token_headers(client: AsyncClient) -> dict[str, str]:
    return await _login_headers(
        client,
        username=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD.get_secret_value(),
        school_slug=None,
    )


@pytest.fixture(scope="session")
async def teacher_token_headers(
    client: AsyncClient, db_session: AsyncSession
) -> dict[str, str]:
    login_identifier = f"teacher-{uuid4().hex[:10]}"
    password = "TeacherPass123!"
    school = await get_or_create_legacy_school(db_session)

    await provision_user_membership(
        db_session,
        school=school,
        shell_role=RoleEnum.TEACHER,
        membership_role_name="teacher",
        login_identifier=login_identifier,
        password=password,
        email=f"{login_identifier}@example.com",
        phone="+251912345678",
        is_active=True,
        is_verified=True,
        mfa_state=MfaStateEnum.VERIFIED,
    )
    await db_session.commit()

    return await _login_headers(
        client,
        username=login_identifier,
        password=password,
        school_slug=school.slug,
    )


@pytest.fixture
async def student_token_headers(
    client: AsyncClient,
    db_session: AsyncSession,
    year_relation: Any,
) -> dict[str, str]:
    login_identifier = f"student-{uuid4().hex[:10]}"
    password = "StudentPass123!"
    school = await get_or_create_legacy_school(db_session)

    user, membership = await provision_user_membership(
        db_session,
        school=school,
        shell_role=RoleEnum.STUDENT,
        membership_role_name="student",
        login_identifier=login_identifier,
        password=password,
        email=f"{login_identifier}@example.com",
        phone="+251912345678",
        is_active=True,
        is_verified=True,
        mfa_state=MfaStateEnum.VERIFIED,
    )

    # /me/student expects a non-null student profile in the current school.
    student_profile = Student(
        school_membership_id=membership.id,
        user_id=user.id,
        registered_for_grade_id=year_relation.grades[0].id,
        first_name="Test",
        father_name="Student",
        grand_father_name="Profile",
        date_of_birth=datetime(2011, 1, 1, tzinfo=timezone.utc).date(),
        gender=GenderEnum.MALE,
        city="Addis Ababa",
        state="Addis Ababa",
        postal_code="1000",
        nationality="Ethiopian",
        blood_type=BloodTypeEnum.UNKNOWN,
        student_photo=None,
        previous_school=None,
        transportation="Bus",
        disability_details=None,
        medical_details=None,
        has_medical_condition=False,
        has_disability=False,
        is_transfer=False,
    )
    student_profile.school_id = school.id
    user.student_profiles.append(student_profile)
    await db_session.commit()

    return await _login_headers(
        client,
        username=login_identifier,
        password=password,
        school_slug=school.slug,
    )


@pytest.fixture
async def token_headers(
    request: pytest.FixtureRequest,
    admin_token_headers,
    teacher_token_headers,
    student_token_headers,
):
    return {
        "admin_token_headers": admin_token_headers,
        "teacher_token_headers": teacher_token_headers,
        "student_token_headers": student_token_headers,
    }[request.param]


@pytest.fixture(scope="session")
async def new_academic_year(
    client: AsyncClient,
    admin_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> NewYearSuccess:
    data = NewYearFactory.create(setup_methods="Default Template")

    r = await client.post(
        f"{settings.API_V1_STR}/years",
        json=data.model_dump(mode="json", by_alias=True),
        headers=admin_token_headers,
    )

    assert r.status_code == 201

    result = NewYearSuccess.model_validate_json(r.text)

    return result


@pytest.fixture(scope="session")
async def year(
    client: AsyncClient,
    admin_token_headers: Dict[str, str],
    new_academic_year: NewYearSuccess,
) -> YearSchema:
    """Test retrieving a single academic year by ID."""
    r = await client.get(
        f"{settings.API_V1_STR}/years/{new_academic_year.id}",
        headers=admin_token_headers,
    )

    assert r.status_code == 200

    year = YearSchema.model_validate_json(r.text)

    return year


@pytest.fixture(scope="session")
async def year_relation(
    client: AsyncClient,
    admin_token_headers: Dict[str, str],
    year: YearSchema,
) -> YearWithRelatedSchema:
    """Retrieving a year with all its relationships."""

    r = await client.get(
        f"{settings.API_V1_STR}/years/{year.id}/relation",
        headers=admin_token_headers,
    )

    assert r.status_code == 200

    year_with_relation = YearWithRelatedSchema.model_validate_json(r.text)

    return year_with_relation


@pytest.fixture(scope="session")
async def grade_relation(
    client: AsyncClient,
    admin_token_headers: Dict[str, str],
    year_relation: YearWithRelatedSchema,
) -> GradeWithRelatedSchema:
    """Retrieving a grade with all its relationships."""

    grade = random.choice(year_relation.grades)

    r = await client.get(
        f"{settings.API_V1_STR}/grades/{grade.id}/relation",
        headers=admin_token_headers,
    )

    assert r.status_code == 200

    grade_with_relation = GradeWithRelatedSchema.model_validate_json(r.text)

    return grade_with_relation


@pytest.fixture(scope="session")
async def streams(
    client: AsyncClient,
    admin_token_headers: Dict[str, str],
    year: YearSchema,
) -> List[StreamSchema]:
    """Test retrieving all streams."""
    r = await client.get(
        f"{settings.API_V1_STR}/streams",
        params={"yearId": str(year.id)},
        headers=admin_token_headers,
    )

    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) > 0

    streams = [StreamSchema.model_validate(stream) for stream in r.json()]

    return streams


@pytest.fixture(scope="session")
async def stream_relation(
    client: AsyncClient,
    admin_token_headers: Dict[str, str],
    streams: List[StreamSchema],
) -> StreamWithRelatedSchema:
    """Retrieving a stream with all its relationships."""

    stream = random.choice(streams)

    r = await client.get(
        f"{settings.API_V1_STR}/streams/{stream.id}/relation",
        headers=admin_token_headers,
    )

    assert r.status_code == 200

    stream_with_relation = StreamWithRelatedSchema.model_validate_json(r.text)

    return stream_with_relation


@pytest.fixture(scope="session")
async def sections(
    client: AsyncClient,
    admin_token_headers: Dict[str, str],
    year_relation: YearWithRelatedSchema,
) -> List[SectionSchema]:
    """Retrieve all sections."""
    grade = random.choice(year_relation.grades)
    r = await client.get(
        f"{settings.API_V1_STR}/sections",
        params={"gradeId": str(grade.id)},
        headers=admin_token_headers,
    )

    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) > 0

    sections = [SectionSchema.model_validate(section) for section in r.json()]

    return sections


@pytest.fixture(scope="session")
async def section_relation(
    client: AsyncClient,
    admin_token_headers: Dict[str, str],
    sections: List[SectionSchema],
) -> SectionWithRelatedSchema:
    """Retrieving a section with all its relationships."""

    section = random.choice(sections)

    r = await client.get(
        f"{settings.API_V1_STR}/sections/{section.id}/relation",
        headers=admin_token_headers,
    )

    assert r.status_code == 200

    section_with_relation = SectionWithRelatedSchema.model_validate_json(r.text)

    return section_with_relation


@pytest.fixture(scope="session")
async def parent(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> Parent:
    """Fixture to create a parent for testing"""

    parent = ParentRegistrationFactory.build()

    r = await client.post(
        f"{settings.API_V1_STR}/register/parents",
        json=parent.model_dump(mode="json", by_alias=True),
        headers=admin_token_headers,
    )

    assert r.status_code == 201

    result = RegistrationResponse.model_validate_json(r.text)

    assert "Parent Registered Successfully" == result.message

    parent = await db_session.get(Parent, result.id)

    assert parent is not None

    return parent
