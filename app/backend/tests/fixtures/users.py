from typing import Awaitable, Callable

import pytest
import pytest_asyncio
from httpx import AsyncClient

from tests.factories.api_data import (
    SignUpFactory,
)
from tests.fixtures import (
    ADMIN_PER_SCHOOL,
    EMPLOYEES_PER_SCHOOL,
    NUM_TEST_USERS,
    STUDENTS_PER_SCHOOL,
)
from tests.utils.api import API
from tests.utils.type_test import (
    MockLogin,
    MockSchool,
    MockSignUp,
    SchoolUsers,
)


@pytest_asyncio.fixture(scope="session")
async def school_users(
    schools: list[MockSchool],
    client: AsyncClient,
) -> list[SchoolUsers]:
    generated = SignUpFactory.create_batch(NUM_TEST_USERS)

    grouped: list[SchoolUsers] = []

    current = 0

    for school in schools:
        admin_users: list[MockSignUp] = []
        student_users: list[MockSignUp] = []
        employee_users: list[MockSignUp] = []

        # Admins
        for _ in range(ADMIN_PER_SCHOOL):
            user = generated[current]
            current += 1

            admin_users.append(await API.signup(client, user))

        # Students
        for _ in range(STUDENTS_PER_SCHOOL):
            user = generated[current]
            current += 1

            student_users.append(await API.signup(client, user))

        # Employees
        for _ in range(EMPLOYEES_PER_SCHOOL):
            user = generated[current]
            current += 1

            employee_users.append(await API.signup(client, user))

        grouped.append(
            SchoolUsers(
                school=school,
                admins=admin_users,
                students=student_users,
                employees=employee_users,
            )
        )

    return grouped


@pytest_asyncio.fixture
async def user(
    request: pytest.FixtureRequest,
    school_users: list[SchoolUsers],
) -> SchoolUsers:
    return school_users[request.param]


@pytest_asyncio.fixture
async def user_login(
    client: AsyncClient,
    school_users: list[SchoolUsers],
) -> Callable[[MockSignUp], Awaitable[MockLogin]]:
    async def _login(
        user: MockSignUp,
    ) -> MockLogin:
        """
        Used to login users who are not a member of a school.
        For example, a user who has signed up but has not yet been added to a school.
        """

        return await API.login(
            client,
            username=user.request.username,
            password=user.request.password,
            school_slug=None,
        )

    return _login
