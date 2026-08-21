import uuid

import pytest
import pytest_asyncio
from httpx import AsyncClient

from project.api.v1.routers.grades.schema import GradeSetupSchema
from project.api.v1.routers.schema import FilterParams
from tests.utils.api import API
from tests.utils.type_test import (
    MockSchool,
    SchoolAdmin,
    SchoolGrade,
    SchoolUsers,
    SchoolYear,
)


@pytest_asyncio.fixture(scope="session")
async def grades(
    client: AsyncClient,
    school_users: list[SchoolUsers],
    school_admins: dict[uuid.UUID, SchoolAdmin],
    years: dict[uuid.UUID, SchoolYear],
) -> dict[uuid.UUID, SchoolGrade]:
    """Fetches grade schemas and sections for each school, keyed by school_id."""
    grades_map: dict[uuid.UUID, SchoolGrade] = {}

    for school_user in school_users:
        school = school_user.school
        school_id = school.response.school_id

        admin = school_admins[school_id].admins[0]

        admin.login.headers["x-school-slug"] = school.request.slug

        r = await API.get_grade_offerings(
            client=client,
            headers=admin.login.headers,
            query=FilterParams(year_id=years[school_id].years[0].id),
        )

        assert r.status_code == 200, f"Expected 200, got {r.status_code}. Response: {r.text}"
        grades_data = [GradeSetupSchema.model_validate(grade) for grade in r.json()]

        assert len(grades_data) > 0, f"No grades found for school with ID {school_id}"

        grades_map[school_id] = SchoolGrade(
            school=school,
            grades=grades_data,
        )

    return grades_map


@pytest_asyncio.fixture(scope="function")
async def grade(
    request: pytest.FixtureRequest,
    schools: list[MockSchool],
    grades: dict[uuid.UUID, SchoolGrade],
) -> SchoolGrade:
    """Returns a single SchoolGrade for the parameterized school."""
    idx: int = request.param

    current_school = schools[idx]
    school_id = current_school.response.school_id

    school_grade = grades.get(school_id)
    if not school_grade or not school_grade.grades:
        raise KeyError(f"No grades found for school_id={school_id}")

    # Returns a single SchoolGrade
    return school_grade
