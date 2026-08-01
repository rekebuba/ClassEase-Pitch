from typing import Awaitable, Callable

import pytest
import pytest_asyncio
from httpx import AsyncClient

from project.core.config import settings
from project.schema.schema import SuccessResponse
from tests.factories.api_data import (
    StudentProfileFactory,
)
from tests.utils.api import API
from tests.utils.type_test import (
    MockSchool,
    MockSignUp,
    MockStudentEnrollment,
    SchoolAdmin,
    SchoolStudent,
    SchoolUsers,
    UserScenario,
)
from tests.utils.utils import find_admin_in_school


@pytest_asyncio.fixture(scope="session")
async def enroll_student(
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

        if not admin:
            raise ValueError(f"No admin membership found for school with ID {school_id}")

        # 1. Create Membership
        student_enrollment = StudentProfileFactory.create(
            user_id=user.response.id,
        )
        admin.login.headers["x-school-slug"] = school.request.slug

        r = await client.post(
            f"{settings.API_V1_STR}/students",
            json=student_enrollment.model_dump(mode="json"),
            headers=admin.login.headers,
        )
        assert r.status_code == 201, f"Expected 201, got {r.status_code}. Response: {r.text}"

        membership = MockStudentEnrollment(
            request=student_enrollment,
            response=SuccessResponse.model_validate(r.json()),
        )

        # 2. Perform Login
        login_data = await API.login(
            client,
            username=user.request.username,
            password=user.request.password,
            school_slug=None,
        )

        student = await API.get_logged_in_user(
            client,
            headers=login_data.headers,
        )

        return UserScenario(
            school=school,
            signup=user,
            user_info=student,
            student=membership,
            login=login_data,
        )

    return _build


@pytest_asyncio.fixture
async def student(
    request: pytest.FixtureRequest,
    student_membership: list[SchoolStudent],
) -> UserScenario:
    return student_membership[request.param].students[0]
