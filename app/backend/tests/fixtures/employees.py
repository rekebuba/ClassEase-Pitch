import uuid
from typing import Awaitable, Callable

import pytest
import pytest_asyncio
from httpx import AsyncClient

from project.api.v1.routers.jobs.schema import JobApplicationPost
from project.schema.models import JobSchema
from project.schema.schema import SuccessResponse
from tests.factories.api_data import (
    HireJobApplicationFactory,
    TeacherProfileFactory,
)
from tests.utils.api import API
from tests.utils.type_test import (
    MockEmployeeProfile,
    MockSchool,
    MockSignUp,
    SchoolAdmin,
    SchoolEmployee,
    SchoolHR,
    SchoolUsers,
    UserScenario,
)
from tests.utils.utils import find_admin_in_school


@pytest_asyncio.fixture(scope="session")
async def submit_employee_application(
    client: AsyncClient,
    school_users: list[SchoolUsers],
    school_hr_data: list[SchoolHR],
) -> Callable[[dict[str, str], JobApplicationPost], Awaitable[SuccessResponse]]:
    async def _submit_employee_application(
        headers: dict[str, str],
        employee_application: JobApplicationPost,
    ) -> SuccessResponse:
        r = await API.post_job_application(
            client=client,
            job_id=employee_application.job_id,
            application_data=employee_application,
            headers=headers,
        )
        assert r.status_code == 201, f"Expected 201, got {r.status_code}. Response: {r.text}"
        return SuccessResponse.model_validate(r.json())

    return _submit_employee_application


@pytest_asyncio.fixture(scope="session")
async def hire_employee(
    client: AsyncClient,
    schools: list[MockSchool],
    school_users: list[SchoolUsers],
    admin_membership: list[SchoolAdmin],
) -> Callable[[MockSchool, MockSignUp, JobApplicationPost, uuid.UUID], Awaitable[UserScenario]]:
    """
    A factory fixture that returns a function to build the scenario.
    """

    async def _build(
        school: MockSchool,
        user: MockSignUp,
        job: JobSchema,
        application_id: uuid.UUID,
    ) -> UserScenario:
        school_id = school.response.school_id

        admin = find_admin_in_school(
            admin_membership=admin_membership,
            school_id=school_id,
        )

        if admin is None:
            raise ValueError(f"No admin membership found for school with ID {school_id}")

        employee_to_hire = HireJobApplicationFactory.create(
            user_id=user.response.id,
            job_id=job.id,
            application_id=application_id,
            manager_employee_id=None,
            teacher_profile=TeacherProfileFactory.create(),
        )

        response = await API.hire_employee(
            client=client,
            employee_data=employee_to_hire,
            headers=admin.login.headers,
        )

        assert response.status_code == 201, f"Expected 201, got {response.status_code}. Response: {response.text}"
        employee_data = SuccessResponse.model_validate(response.json())
        assert employee_data is not None, "Failed to validate response JSON"

        login_data = await API.login(
            client,
            username=user.request.username,
            password=user.request.password,
            school_slug=None,
        )

        user_info = await API.get_logged_in_user(
            client,
            headers=login_data.headers,
        )

        return UserScenario(
            school=school,
            signup=user,
            user_info=user_info,
            employee=MockEmployeeProfile(
                request=employee_to_hire,
                response=employee_data,
            ),
            login=login_data,
        )

    return _build


@pytest_asyncio.fixture
async def employee(
    request: pytest.FixtureRequest,
    employee_membership: list[SchoolEmployee],
) -> UserScenario:
    return employee_membership[request.param]
