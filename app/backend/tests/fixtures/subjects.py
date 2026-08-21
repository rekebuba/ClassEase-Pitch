import uuid

import pytest
import pytest_asyncio
from httpx import AsyncClient

from project.api.v1.routers.schema import FilterParams
from project.api.v1.routers.subjects.schema import SubjectSetupSchema
from tests.utils.api import API
from tests.utils.type_test import (
    MockSchool,
    SchoolAdmin,
    SchoolSubject,
    SchoolUsers,
    SchoolYear,
)


@pytest_asyncio.fixture(scope="session")
async def subjects(
    client: AsyncClient,
    school_users: list[SchoolUsers],
    school_admins: dict[uuid.UUID, SchoolAdmin],
    years: dict[uuid.UUID, SchoolYear],
) -> dict[uuid.UUID, SchoolSubject]:
    """Fetches subject schemas and sections for each school, keyed by school_id."""
    subjects_map: dict[uuid.UUID, SchoolSubject] = {}

    for school_user in school_users:
        school = school_user.school
        school_id = school.response.school_id

        admin = school_admins[school_id].admins[0]

        admin.login.headers["x-school-slug"] = school.request.slug

        r = await API.get_subject_offerings(
            client=client,
            headers=admin.login.headers,
            query=FilterParams(year_id=years[school_id].years[0].id),
        )

        assert r.status_code == 200, f"Expected 200, got {r.status_code}. Response: {r.text}"
        subjects_data = [SubjectSetupSchema.model_validate(subject) for subject in r.json()]

        assert len(subjects_data) > 0, f"No subjects found for school with ID {school_id}"

        subjects_map[school_id] = SchoolSubject(
            school=school,
            subjects=subjects_data,
        )

    return subjects_map


@pytest_asyncio.fixture(scope="function")
async def subject(
    request: pytest.FixtureRequest,
    schools: list[MockSchool],
    subjects: dict[uuid.UUID, SchoolSubject],
) -> SchoolSubject:
    """Returns a single SchoolSubject for the parameterized school."""
    idx: int = request.param

    current_school = schools[idx]
    school_id = current_school.response.school_id

    school_subject = subjects.get(school_id)
    if not school_subject or not school_subject.subjects:
        raise KeyError(f"No subjects found for school_id={school_id}")

    # Returns a single SchoolSubject
    return school_subject
