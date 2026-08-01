from typing import Awaitable, Callable

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from project.api.v1.routers.school.schema import (
    SuccessSchoolResponse,
)
from project.core.config import settings
from project.models import (
    AcademicTerm,
    AssessmentScheme,
    AssessmentSchemeComponent,
    ClassSection,
    Grade,
    Section,
    Stream,
    Subject,
    SubjectOffering,
    Year,
)
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
    SchoolScenario,
    SchoolStudent,
    SchoolYear,
    YearScenario,
)
from tests.utils.utils import _count_rows, find_admin_in_school

PROVISIONED_MODELS = (
    Year,
    AcademicTerm,
    Subject,
    Grade,
    Section,
    Stream,
    AssessmentScheme,
    AssessmentSchemeComponent,
    SubjectOffering,
    ClassSection,
)


@pytest_asyncio.fixture(scope="session")
async def schools(
    client: AsyncClient,
    owner_token_headers: MockLogin,
) -> list[MockSchool]:
    created: list[MockSchool] = []
    generated = NewSchoolFactory.create_batch(NUM_TEST_SCHOOLS)

    for school in generated:
        r = await client.post(
            f"{settings.API_V1_STR}/schools",
            json=school.model_dump(mode="json"),
            headers=owner_token_headers.headers,
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
    employee_membership: list[SchoolEmployee],
    student_membership: list[SchoolStudent],
    admin_membership: list[SchoolAdmin],
    years: list[SchoolYear],
    grades: list[SchoolGrade],
) -> SchoolScenario:
    idx = request.param

    # Defensive check: Ensure we are pulling data for the exact same school
    current_school = schools[idx]
    assert employee_membership[idx].school == current_school
    assert student_membership[idx].school == current_school
    assert admin_membership[idx].school == current_school
    assert years[idx].school == current_school
    assert grades[idx].school == current_school

    all_users = []
    all_users.extend(admin_membership[idx].admins)
    all_users.extend(employee_membership[idx].employees)
    all_users.extend(student_membership[idx].students)

    return SchoolScenario(
        school=schools[idx],
        users=all_users,
        years=years[idx],
        grades=grades[idx],
    )


@pytest_asyncio.fixture(scope="session")
async def default_school_setup(
    client: AsyncClient,
    db_session: AsyncSession,
    schools: list[MockSchool],
    admin_membership: list[SchoolAdmin],
) -> Callable[[MockSchool, MockSignUp], Awaitable[YearScenario]]:
    """
    A factory fixture that returns a function to build the scenario.
    """

    async def _build(
        school: MockSchool,
        user: MockSignUp,
    ) -> YearScenario:
        school_id = school.response.school_id

        admin = find_admin_in_school(
            admin_membership=admin_membership,
            school_id=school_id,
        )

        if not admin:
            raise ValueError(f"No admin membership found for school with ID {school_id}")

        new_year = NewYearFactory.create(
            setup_methods="Default Template",
            status=AcademicYearStatusEnum.ACTIVE,
        )
        admin.login.headers["x-school-slug"] = school.request.slug

        year = await API.post_year(
            client=client,
            new_year=new_year,
            headers=admin.login.headers,
        )

        counts = {
            model.__tablename__: await _count_rows(
                tenant_session=db_session,
                model=model,
                school_id=school_id,
            )
            for model in PROVISIONED_MODELS
        }

        assert counts["years"] == 1
        assert counts["academic_terms"] == 2
        assert counts["subjects"] >= 20
        assert counts["grades"] == 12
        assert counts["sections"] >= 36
        assert counts["streams"] >= 2
        assert counts["assessment_schemes"] == 1
        assert counts["assessment_scheme_components"] == 4
        assert counts["subject_offerings"] == 130
        assert counts["class_sections"] > 0

        return YearScenario(
            school=school,
            year=year,
        )

    return _build
