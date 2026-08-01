from typing import Awaitable, Callable

import pytest
import pytest_asyncio
from httpx import AsyncClient

from tests.factories.api_data import (
    EmployeeProfileFactory,
    TeacherProfileFactory,
)
from tests.utils.api import API
from tests.utils.type_test import (
    MockSchool,
    MockSignUp,
    SchoolAdmin,
    SchoolEmployee,
    SchoolUsers,
    UserScenario,
)
from tests.utils.utils import find_admin_in_school


@pytest_asyncio.fixture(scope="session")
async def hire_employee(
    client: AsyncClient,
    schools: list[MockSchool],
    school_users: list[SchoolUsers],
    admin_membership: list[SchoolAdmin],
) -> Callable[[MockSchool, MockSignUp], Awaitable[UserScenario]]:
    """
    A factory fixture that returns a function to build the scenario.
    """

    async def _build(
        school: MockSchool,
        user: MockSignUp,
    ) -> UserScenario:
        school_id = school.response.school_id

        admin = find_admin_in_school(
            admin_membership=admin_membership,
            school_id=school_id,
        )

        if admin is None:
            raise ValueError(f"No admin membership found for school with ID {school_id}")

        # 1. Create Membership
        employee_profile = EmployeeProfileFactory.create(
            user_id=user.response.id,
            department_id=None,
            manager_employee_id=None,
            primary_position_id=None,
        )

        membership = await API.post_employee(
            client=client,
            employee_profile=employee_profile,
            headers=admin.login.headers,
        )

        teacher_profile = TeacherProfileFactory.create(
            employee_id=membership.response.id,
        )

        await API.post_teacher_profile(
            client=client,
            teacher_profile=teacher_profile,
            headers=admin.login.headers,
        )

        # 2. Perform Login
        login_data = await API.login(
            client,
            username=user.request.username,
            password=user.request.password,
            school_slug=None,
        )

        employee = await API.get_logged_in_user(
            client,
            headers=login_data.headers,
        )

        return UserScenario(
            school=school,
            signup=user,
            user_info=employee,
            employee=membership,
            login=login_data,
        )

    return _build


@pytest_asyncio.fixture
async def employee(
    request: pytest.FixtureRequest,
    employee_membership: list[SchoolEmployee],
) -> UserScenario:
    return employee_membership[request.param]
