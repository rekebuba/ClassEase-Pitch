import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from project.utils.enum import (
    RoleEnum,
)
from tests.api.routers.test_login import _create_multi_school_user
from tests.utils.api import API
from tests.utils.type_test import SchoolScenario


@pytest.fixture(scope="session")
async def multi_school_user(db_session: AsyncSession) -> dict[str, str]:
    return await _create_multi_school_user(db_session, password="MultiSchoolPass123!")


@pytest.mark.parametrize(
    "role",
    [
        RoleEnum.ADMIN,
        RoleEnum.TEACHER,
        RoleEnum.STUDENT,
    ],
)
async def test_private_endpoints_require_auth(
    client: AsyncClient,
    role: RoleEnum,
    school: SchoolScenario,
) -> None:
    await API.get_logged_in_user(
        client,
        headers=school.find_user(lambda u: u.user_info.role == role).login.headers,
    )


async def test_me_supports_multi_school_memberships(
    client: AsyncClient,
    multi_school_user: dict[str, str],
) -> None:
    primary_headers = await API.login(
        client,
        username=multi_school_user["username"],
        password=multi_school_user["password"],
        school_slug=multi_school_user["primary_school_slug"],
    )
    secondary_headers = await API.login(
        client,
        username=multi_school_user["username"],
        password=multi_school_user["password"],
        school_slug=multi_school_user["secondary_school_slug"],
    )

    primary_response = await API.get_logged_in_user(
        client,
        headers=primary_headers.headers,
    )
    secondary_response = await API.get_logged_in_user(
        client,
        headers=secondary_headers.headers,
    )

    assert primary_response.active_school.slug == multi_school_user["primary_school_slug"]
    assert secondary_response.active_school.slug == multi_school_user["secondary_school_slug"]

    primary_slugs = {membership.school_slug for membership in primary_response.available_memberships}
    secondary_slugs = {membership.school_slug for membership in secondary_response.available_memberships}
    expected_slugs = {
        multi_school_user["primary_school_slug"],
        multi_school_user["secondary_school_slug"],
    }

    assert expected_slugs.issubset(primary_slugs)
    assert expected_slugs.issubset(secondary_slugs)
