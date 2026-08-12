import uuid
from typing import Awaitable, Callable

import pytest
import pytest_asyncio
from httpx import AsyncClient

from project.api.v1.routers.jobs.schema import JobApplicationPost
from project.api.v1.routers.school.schema import (
    SuccessNewSchoolMembership,
)
from project.core.config import settings
from project.schema.schema import SuccessResponse
from project.utils.enum import RoleEnum
from tests.factories.api_data import (
    JobApplicationFactory,
    NewSchoolMembershipFactory,
)
from tests.utils.api import API
from tests.utils.type_test import (
    MockLogin,
    MockSchool,
    MockSchoolMembership,
    MockSignUp,
    SchoolAdmin,
    SchoolEmployee,
    SchoolHR,
    SchoolStudent,
    SchoolUsers,
    UserScenario,
)


@pytest_asyncio.fixture(scope="session")
async def school_membership(
    client: AsyncClient,
    schools: list[MockSchool],
    school_users: list[SchoolUsers],
    owner_token_headers: MockLogin,
) -> Callable[[MockSchool, MockSignUp, RoleEnum], Awaitable[UserScenario]]:
    """
    A factory fixture that returns a function to build the scenario.
    """

    async def _build(
        school: MockSchool,
        user: MockSignUp,
        role: RoleEnum,
    ) -> UserScenario:
        new_membership = NewSchoolMembershipFactory.create(
            user_id=user.response.id,
            role=role,
        )
        r = await client.post(
            f"{settings.API_V1_STR}/schools/{school.response.school_id}/membership",
            json=new_membership.model_dump(mode="json"),
            headers=owner_token_headers.headers,
        )

        assert r.status_code == 201, f"Expected 201, got {r.status_code}. Response: {r.text}"

        membership = MockSchoolMembership(
            request=new_membership,
            response=SuccessNewSchoolMembership.model_validate(r.json()),
        )

        # 2. Perform Login
        login_data = await API.login(
            client,
            username=user.request.username,
            password=user.request.password,
            school_slug=None,
        )

        admin = await API.get_logged_in_user(
            client,
            headers=login_data.headers,
        )

        return UserScenario(
            school=school,
            signup=user,
            user_info=admin,
            membership=membership,
            login=login_data,
        )

    return _build


@pytest_asyncio.fixture(scope="session")
async def admin_membership(
    school_membership: Callable[[MockSchool, MockSignUp, RoleEnum], Awaitable[UserScenario]],
    school_users: list[SchoolUsers],
) -> list[SchoolAdmin]:
    school: list[SchoolAdmin] = []

    for users in school_users:
        admins: list[UserScenario] = []

        for admin in users.admins:
            admins.append(await school_membership(users.school, admin, RoleEnum.ADMIN))

        school.append(SchoolAdmin(school=users.school, admins=admins))

    return school


@pytest_asyncio.fixture
async def admin(
    request: pytest.FixtureRequest,
    admin_membership: list[SchoolAdmin],
) -> SchoolAdmin:
    return admin_membership[request.param]


@pytest_asyncio.fixture(scope="session")
async def employee_membership(
    client: AsyncClient,
    school_users: list[SchoolUsers],
    school_hr_data: list[SchoolHR],
    submit_employee_application: Callable[
        [dict[str, str], JobApplicationPost],
        Awaitable[SuccessResponse],
    ],
    hire_employee: Callable[
        [MockSchool, MockSignUp, JobApplicationPost, uuid.UUID],
        Awaitable[UserScenario],
    ],
) -> list[SchoolEmployee]:
    """Hire employees in each school."""

    school_employees: list[SchoolEmployee] = []

    for school_users_data, school_hr in zip(
        school_users,
        school_hr_data,
        strict=True,
    ):
        hired_employees: list[UserScenario] = []

        for i, employee in enumerate(school_users_data.employees):
            job = school_hr.jobs[i]

            assert len(school_users_data.employees) <= len(school_hr.jobs), "Not enough jobs available for employees."

            login = await API.login(
                client,
                username=employee.request.username,
                password=employee.request.password,
                school_slug=None,
            )

            job_application = JobApplicationFactory.create(
                school_id=job.school_id,
                user_id=employee.response.id,
                job_id=job.id,
            )

            application = await submit_employee_application(
                login.headers,
                job_application,
            )

            hired_employee = await hire_employee(
                school_users_data.school,
                employee,
                job,
                application.id,
            )

            hired_employees.append(hired_employee)

        school_employees.append(
            SchoolEmployee(
                school=school_users_data.school,
                employees=hired_employees,
            )
        )

    return school_employees


@pytest_asyncio.fixture(scope="session")
async def student_membership(
    school_users: list[SchoolUsers],
    enroll_student: Callable[[MockSchool, MockSignUp], Awaitable[UserScenario]],
) -> list[SchoolStudent]:
    """Fixture to enroll a student in a school"""
    schools: list[SchoolStudent] = []

    for users in school_users:
        students: list[UserScenario] = []

        for student in users.students:
            students.append(await enroll_student(users.school, student))

        schools.append(SchoolStudent(school=users.school, students=students))

    return schools
