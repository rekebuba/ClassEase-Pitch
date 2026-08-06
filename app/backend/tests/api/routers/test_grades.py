import pytest
from httpx import AsyncClient

from project.api.v1.routers.schema import FilterParams
from project.utils.enum import RoleEnum
from tests.utils.api import API
from tests.utils.type_test import SchoolScenario


@pytest.mark.parametrize(
    "role, search, expected_count",
    [
        (RoleEnum.ADMIN, None, 12),
        (RoleEnum.ADMIN, "hjgkjknmm", 0),
        (RoleEnum.ADMIN, "grade", 12),
        (RoleEnum.ADMIN, "grade 5", 1),
        (RoleEnum.ADMIN, "grade 0", 1),  # Grade 10
        (RoleEnum.ADMIN, "grade 1", 4),
        (RoleEnum.ADMIN, "", 12),
    ],
)
async def test_get_grades_offerings(
    client: AsyncClient,
    school: SchoolScenario,
    role: RoleEnum,
    search: str | None,
    expected_count: int,
) -> None:
    """
    Test the get_grades_offerings function for different user roles.
    """
    headers = school.find_user(lambda u: u.user_info.role == role).login.headers

    result = await API.get_grades_offerings(
        client=client,
        headers=headers,
        query=FilterParams(year_id=school.years[0].year.response.id, q=search),
    )

    assert len(result) == expected_count, f"Expected {expected_count}, got {len(result)}"


@pytest.mark.parametrize(
    "role",
    [
        RoleEnum.ADMIN,
    ],
)
async def test_get_grade_offerings_by_id(client: AsyncClient, school: SchoolScenario, role: RoleEnum) -> None:
    """
    Test the get_grade_offerings_by_id function for different user roles.
    """
    headers = school.find_user(lambda u: u.user_info.role == role).login.headers

    grades = await API.get_grades_offerings(
        client=client,
        headers=headers,
        query=FilterParams(year_id=school.years[0].year.response.id),
    )

    await API.get_grade_offerings_by_id(
        client=client,
        headers=headers,
        grade_id=grades[0].id,
    )
