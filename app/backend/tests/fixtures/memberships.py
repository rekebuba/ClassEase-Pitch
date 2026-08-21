import uuid
from typing import Awaitable, Callable

import pytest
import pytest_asyncio
from httpx import AsyncClient

from project.api.v1.routers.school.schema import (
    SuccessNewSchoolMembership,
)
from project.core.config import settings
from project.utils.enum import RoleEnum
from tests.factories.api_data import (
    NewSchoolMembershipFactory,
)
from tests.utils.api import API
from tests.utils.type_test import (
    MockLogin,
    MockSchool,
    MockSchoolMembership,
    MockSignUp,
    SchoolAdmin,
    SchoolUsers,
    UserScenario,
)


@pytest_asyncio.fixture(scope="session")
async def school_membership(
    client: AsyncClient,
    schools: list[MockSchool],
    school_users: list[SchoolUsers],
    super_user: MockLogin,
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
            headers=super_user.headers,
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
async def school_admins(
    school_users: list[SchoolUsers],
    school_membership: Callable[[MockSchool, MockSignUp, RoleEnum], Awaitable[UserScenario]],
) -> dict[uuid.UUID, SchoolAdmin]:
    admins_map: dict[uuid.UUID, SchoolAdmin] = {}

    for users in school_users:
        school = users.school
        school_id = school.response.school_id
        admins: list[UserScenario] = []

        for admin in users.admins:
            admins.append(await school_membership(users.school, admin, RoleEnum.ADMIN))

        admins_map[school_id] = SchoolAdmin(school=users.school, admins=admins)

    return admins_map


@pytest_asyncio.fixture
async def admin(
    request: pytest.FixtureRequest,
    schools: list[MockSchool],
    school_admins: dict[uuid.UUID, SchoolAdmin],
) -> SchoolAdmin:
    """Returns a single SchoolAdmin for the parameterized school."""
    idx: int = request.param

    current_school = schools[idx]
    school_id = current_school.response.school_id

    school_admin = school_admins.get(school_id)
    if not school_admin:
        raise KeyError(f"No admin found for school_id={school_id}")

    # Returns a single SchoolAdmin matching the return type -> SchoolAdmin
    return school_admin
