import uuid
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


@pytest_asyncio.fixture(scope="session")
async def enroll_student(
    client: AsyncClient,
    schools: list[MockSchool],
    school_users: list[SchoolUsers],
    school_admins: dict[uuid.UUID, SchoolAdmin],
) -> Callable[[MockSchool, MockSignUp], Awaitable[UserScenario]]:
    """
    A factory fixture that returns a function to build the scenario.
    """

    async def _build(
        school: MockSchool,
        user: MockSignUp,
    ) -> UserScenario:
        school_id = school.response.school_id
        admin = school_admins[school_id].admins[0]

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
    school_students: list[SchoolStudent],
) -> UserScenario:
    return school_students[request.param].students[0]
