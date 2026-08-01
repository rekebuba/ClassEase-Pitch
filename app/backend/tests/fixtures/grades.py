from typing import Awaitable, Callable

import pytest
import pytest_asyncio
from httpx import AsyncClient

from project.schema.models import GradeSchema
from tests.utils.api import API
from tests.utils.type_test import (
    GradeScenario,
    SchoolAdmin,
    SchoolGrade,
    SchoolUsers,
    SectionScenario,
)
from tests.utils.utils import find_admin_in_school


@pytest_asyncio.fixture(scope="session")
async def get_grades(
    client: AsyncClient,
) -> Callable[[dict[str, str]], Awaitable[list[GradeSchema]]]:
    async def _get_grades(headers: dict[str, str]) -> list[GradeSchema]:
        return await API.get_grades(
            client=client,
            headers=headers,
        )

    return _get_grades


@pytest_asyncio.fixture(scope="session")
async def grades(
    client: AsyncClient,
    school_users: list[SchoolUsers],
    admin_membership: list[SchoolAdmin],
    get_grades: Callable[[dict[str, str]], Awaitable[list[GradeSchema]]],
) -> list[SchoolGrade]:
    schools: list[SchoolGrade] = []

    for school in school_users:
        grades = []
        school_id = school.school.response.school_id

        admin = find_admin_in_school(
            admin_membership=admin_membership,
            school_id=school_id,
        )

        if not admin:
            raise ValueError(f"No admin membership found for school with ID {school_id}")

        admin.login.headers["x-school-slug"] = school.school.request.slug

        grades_data = await get_grades(admin.login.headers)

        assert len(grades_data) > 0, f"No grades found for school with ID {school_id}"

        for grade in grades_data:
            sections = await API.get_sections(
                client=client,
                headers=admin.login.headers,
                grade_id=grade.id,
            )

            section_scenario = SectionScenario(grade=grade, sections=sections)

            grade_scenario = GradeScenario(school=school.school, grade=grade, sections=section_scenario)

            grades.append(grade_scenario)

        schools.append(SchoolGrade(school=school.school, grades=grades))
    return schools


@pytest_asyncio.fixture(scope="function")
async def grade(
    request: pytest.FixtureRequest,
    grades: list[SchoolGrade],
) -> GradeScenario:
    idx = request.param

    # Defensive check: Ensure we are pulling data for the exact same school
    current_school = grades[idx].school
    assert grades[idx].school == current_school

    return grades[idx]
