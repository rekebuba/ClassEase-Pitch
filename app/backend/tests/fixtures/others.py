import random
from typing import List

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from project.api.v1.routers.registrations.schema import RegistrationResponse
from project.core.config import settings
from project.models import Parent
from project.schema.models import (
    GradeWithRelatedSchema,
    SectionSchema,
    SectionWithRelatedSchema,
    StreamSchema,
    YearSchema,
    YearWithRelatedSchema,
)
from project.schema.models.stream_schema import StreamWithRelatedSchema
from tests.factories.api_data import (
    ParentRegistrationFactory,
)
from tests.utils.type_test import (
    MockSchool,
    SchoolAdmin,
)


@pytest.fixture(scope="session")
async def teacher_token_headers(
    client: AsyncClient,
    db_session: AsyncSession,
    school: MockSchool,
):
    pass


@pytest.fixture
async def student_token_headers(
    client: AsyncClient,
    db_session: AsyncSession,
    school: MockSchool,
):
    pass


@pytest.fixture(scope="session")
async def year_relation(
    client: AsyncClient,
    admin: SchoolAdmin,
    year: YearSchema,
) -> YearWithRelatedSchema:
    """Retrieving a year with all its relationships."""

    r = await client.get(
        f"{settings.API_V1_STR}/years/{year.id}/relation",
        headers=admin.login.headers,
    )

    assert r.status_code == 200

    year_with_relation = YearWithRelatedSchema.model_validate_json(r.text)

    return year_with_relation


@pytest.fixture(scope="session")
async def grade_relation(
    client: AsyncClient,
    admin: SchoolAdmin,
    year_relation: YearWithRelatedSchema,
) -> GradeWithRelatedSchema:
    """Retrieving a grade with all its relationships."""

    grade = random.choice(year_relation.grades)

    r = await client.get(
        f"{settings.API_V1_STR}/grades/{grade.id}/relation",
        headers=admin.login.headers,
    )

    assert r.status_code == 200

    grade_with_relation = GradeWithRelatedSchema.model_validate_json(r.text)

    return grade_with_relation


@pytest.fixture(scope="session")
async def streams(
    client: AsyncClient,
    admin: SchoolAdmin,
    year: YearSchema,
) -> List[StreamSchema]:
    """Test retrieving all streams."""
    r = await client.get(
        f"{settings.API_V1_STR}/streams",
        params={"yearId": str(year.id)},
        headers=admin.login.headers,
    )

    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) > 0

    streams = [StreamSchema.model_validate(stream) for stream in r.json()]

    return streams


@pytest.fixture(scope="session")
async def stream_relation(
    client: AsyncClient,
    admin: SchoolAdmin,
    streams: List[StreamSchema],
) -> StreamWithRelatedSchema:
    """Retrieving a stream with all its relationships."""

    stream = random.choice(streams)

    r = await client.get(
        f"{settings.API_V1_STR}/streams/{stream.id}/relation",
        headers=admin.login.headers,
    )

    assert r.status_code == 200

    stream_with_relation = StreamWithRelatedSchema.model_validate_json(r.text)

    return stream_with_relation


@pytest.fixture(scope="session")
async def sections(
    client: AsyncClient,
    admin: SchoolAdmin,
    year_relation: YearWithRelatedSchema,
) -> List[SectionSchema]:
    """Retrieve all sections."""
    grade = random.choice(year_relation.grades)
    r = await client.get(
        f"{settings.API_V1_STR}/sections",
        params={"gradeId": str(grade.id)},
        headers=admin.login.headers,
    )

    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) > 0

    sections = [SectionSchema.model_validate(section) for section in r.json()]

    return sections


@pytest.fixture(scope="session")
async def section_relation(
    client: AsyncClient,
    admin: SchoolAdmin,
    sections: List[SectionSchema],
) -> SectionWithRelatedSchema:
    """Retrieving a section with all its relationships."""

    section = random.choice(sections)

    r = await client.get(
        f"{settings.API_V1_STR}/sections/{section.id}/relation",
        headers=admin.login.headers,
    )

    assert r.status_code == 200

    section_with_relation = SectionWithRelatedSchema.model_validate_json(r.text)

    return section_with_relation


@pytest.fixture(scope="session")
async def parent(
    client: AsyncClient,
    db_session: AsyncSession,
    admin: SchoolAdmin,
) -> Parent:
    """Fixture to create a parent for testing"""

    parent = ParentRegistrationFactory.build()

    r = await client.post(
        f"{settings.API_V1_STR}/register/parents",
        json=parent.model_dump(mode="json", by_alias=True),
        headers=admin.login.headers,
    )

    assert r.status_code == 201, f"Expected 201, got {r.status_code}. Response: {r.text}"

    result = RegistrationResponse.model_validate_json(r.text)

    assert "Parent Registered Successfully" == result.message

    parent = await db_session.get(Parent, result.id)

    assert parent is not None

    return parent
