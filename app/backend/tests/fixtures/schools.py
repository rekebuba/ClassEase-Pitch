import uuid
from typing import Awaitable, Callable

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from project.api.v1.routers.school.schema import (
    SuccessSchoolResponse,
)
from project.core.config import settings
from project.schema.models import YearSchema
from project.schema.schema import SuccessResponse
from project.utils.enum import AcademicYearStatusEnum
from tests.factories.api_data import (
    NewSchoolFactory,
    NewYearFactory,
)
from tests.fixtures import NUM_TEST_SCHOOLS
from tests.utils.api import API
from tests.utils.type_test import (
    MockLogin,
    MockSchool,
    MockSignUp,
    SchoolAdmin,
    SchoolEmployee,
    SchoolGrade,
    SchoolHR,
    SchoolScenario,
    SchoolStudent,
    SchoolSubject,
    SchoolYear,
)
from tests.utils.utils import _assert_provisioned_models_counts


@pytest_asyncio.fixture(scope="session")
async def schools(
    client: AsyncClient,
    super_user: MockLogin,
) -> list[MockSchool]:
    created: list[MockSchool] = []
    generated = NewSchoolFactory.create_batch(NUM_TEST_SCHOOLS)

    for school in generated:
        r = await client.post(
            f"{settings.API_V1_STR}/schools",
            json=school.model_dump(mode="json"),
            headers=super_user.headers,
        )
        assert r.status_code == 201, f"Expected 201, got {r.status_code}. Response: {r.text}"
        created.append(
            MockSchool(
                request=school,
                response=SuccessSchoolResponse.model_validate(r.json()),
            )
        )

    return created


@pytest_asyncio.fixture
async def school(
    request: pytest.FixtureRequest,
    schools: list[MockSchool],
    school_hr_data: dict[uuid.UUID, SchoolHR],
    school_admins: dict[uuid.UUID, SchoolAdmin],
    school_employees: dict[uuid.UUID, SchoolEmployee],
    school_students: dict[uuid.UUID, SchoolStudent],
    years: dict[uuid.UUID, SchoolYear],
    grades: dict[uuid.UUID, SchoolGrade],
    subjects: dict[uuid.UUID, SchoolSubject],
) -> SchoolScenario:
    idx = request.param

    # Defensive check: Ensure we are pulling data for the exact same school
    current_school = schools[idx]
    school_id = current_school.response.school_id

    admins = school_admins[school_id]
    employees = school_employees[school_id]
    students = school_students[school_id]
    hr_data = school_hr_data[school_id]
    years_data = years[school_id]
    grades_data = grades[school_id]
    subjects_data = subjects[school_id]

    all_users = [*admins.admins, *employees.employees, *students.students]

    return SchoolScenario(
        school=schools[idx],
        users=all_users,
        years=years_data,
        grades=grades_data,
        subjects=subjects_data,
        hr=hr_data,
    )


@pytest_asyncio.fixture(scope="session")
async def default_school_setup(
    client: AsyncClient,
    db_session: AsyncSession,
    schools: list[MockSchool],
    school_admins: dict[uuid.UUID, SchoolAdmin],
) -> Callable[[MockSchool, MockSignUp], Awaitable[SchoolYear]]:
    """
    A factory fixture that returns a function to build the scenario.
    """

    async def _build(
        school: MockSchool,
        user: MockSignUp,
    ) -> SchoolYear:
        school_id = school.response.school_id

        admin = school_admins[school_id].admins[0]
        new_year = NewYearFactory.create(
            setup_methods="Default Template",
            status=AcademicYearStatusEnum.ACTIVE,
        )
        admin.login.headers["x-school-slug"] = school.request.slug

        r = await API.post_year(
            client=client,
            new_year=new_year,
            headers=admin.login.headers,
        )

        assert r.status_code == 201, f"Expected 201, got {r.status_code}. Response: {r.text}"
        assert SuccessResponse.model_validate(r.json()) is not None, "Failed to create a new academic year."

        await _assert_provisioned_models_counts(
            tenant_session=db_session,
            school_id=school_id,
        )

        r = await API.get_years(
            client=client,
            headers=admin.login.headers,
        )

        assert r.status_code == 200, f"Expected 200, got {r.status_code}. Response: {r.text}"
        assert type(r.json()) is list, f"Expected a list of academic years, got {type(r.json())}"
        years = [YearSchema.model_validate(year) for year in r.json()]

        return SchoolYear(
            school=school,
            years=years,
        )

    return _build
