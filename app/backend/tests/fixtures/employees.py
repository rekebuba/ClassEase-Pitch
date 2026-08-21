import uuid
from typing import Awaitable, Callable

import pytest
import pytest_asyncio
from httpx import AsyncClient

from project.schema.schema import SuccessResponse
from tests.factories.api_data import (
    HireJobApplicationFactory,
    JobApplicationFactory,
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


@pytest_asyncio.fixture(scope="session")
async def hire_employee(
    client: AsyncClient,
    schools: list[MockSchool],
    school_users: list[SchoolUsers],
    school_admins: dict[uuid.UUID, SchoolAdmin],
) -> Callable[[MockSchool, MockSignUp, uuid.UUID], Awaitable[UserScenario]]:
    """
    A factory fixture that returns a function to build the scenario.
    """

    async def _build(
        school: MockSchool,
        user: MockSignUp,
        application_id: uuid.UUID,
    ) -> UserScenario:
        school_id = school.response.school_id

        admin = school_admins[school_id].admins[0]

        employee_to_hire = HireJobApplicationFactory.create(
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


@pytest_asyncio.fixture(scope="session")
async def school_employees(
    client: AsyncClient,
    school_users: list[SchoolUsers],
    school_hr_data: dict[uuid.UUID, SchoolHR],
    hire_employee: Callable[
        [MockSchool, MockSignUp, uuid.UUID],
        Awaitable[UserScenario],
    ],
) -> dict[uuid.UUID, SchoolEmployee]:
    """Hire employees for each school and return a map keyed by school_id."""

    employees_by_school: dict[uuid.UUID, SchoolEmployee] = {}

    for school_users_data in school_users:
        school = school_users_data.school
        school_id = school.response.school_id

        school_hr = school_hr_data.get(school_id)
        if not school_hr:
            raise KeyError(f"No HR data setup for school_id={school_id}")

        hired_employees: list[UserScenario] = []

        assert len(school_users_data.employees) <= len(school_hr.jobs), (
            f"Not enough jobs for school {school_id}: "
            f"{len(school_users_data.employees)} employees, "
            f"{len(school_hr.jobs)} jobs"
        )

        # Iterate directly over matched jobs for this specific school
        for employee, job in zip(school_users_data.employees, school_hr.jobs):
            login = await API.login(
                client,
                username=employee.request.username,
                password=employee.request.password,
                school_slug=None,
            )

            job_application = JobApplicationFactory.create(
                job_id=job.id,
            )

            # submit the job application
            r = await API.post_job_application(
                client=client,
                application_data=job_application,
                headers=login.headers,
            )
            assert r.status_code == 201, f"Expected 201, got {r.status_code}. Response: {r.text}"
            application = SuccessResponse.model_validate(r.json())

            hired_employee = await hire_employee(
                school,
                employee,
                application.id,
            )

            hired_employees.append(hired_employee)

        employees_by_school[school_id] = SchoolEmployee(
            school=school,
            employees=hired_employees,
        )

    return employees_by_school


@pytest_asyncio.fixture
async def employee(
    request: pytest.FixtureRequest,
    schools: list[MockSchool],
    school_employees: dict[uuid.UUID, SchoolEmployee],
) -> SchoolEmployee:
    """Returns a single SchoolEmployee for the parameterized school."""
    idx: int = request.param

    current_school = schools[idx]
    school_id = current_school.response.school_id

    school_employee = school_employees.get(school_id)
    if not school_employee or not school_employee.employees:
        raise KeyError(f"No employees found for school_id={school_id}")

    # Returns a single SchoolEmployee
    return school_employee
