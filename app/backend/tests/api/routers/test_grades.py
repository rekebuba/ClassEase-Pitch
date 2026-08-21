import pytest
from httpx import AsyncClient

from project.api.v1.routers.grades.schema import GradeSetupSchema
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
async def test_get_grade_offerings(
    client: AsyncClient,
    school: SchoolScenario,
    role: RoleEnum,
    search: str | None,
    expected_count: int,
) -> None:
    """
    Test the get_grade_offerings function for different user roles.
    """
    headers = school.find_user(lambda u: u.user_info.role == role).login.headers

    r = await API.get_grade_offerings(
        client=client,
        headers=headers,
        query=FilterParams(year_id=school.years.years[0].id, q=search),
    )

    assert r.status_code == 200, f"Expected 200, got {r.status_code}. Response: {r.text}"
    grade_offerings = [GradeSetupSchema.model_validate(grade) for grade in r.json()]

    assert len(grade_offerings) == expected_count, f"Expected {expected_count}, got {len(grade_offerings)}"


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

    r = await API.get_grade_offerings(
        client=client,
        headers=headers,
        query=FilterParams(year_id=school.years.years[0].id),
    )

    assert r.status_code == 200, f"Expected 200, got {r.status_code}. Response: {r.text}"
    grade_offerings = [GradeSetupSchema.model_validate(grade) for grade in r.json()]

    r = await API.get_grade_offerings_by_id(
        client=client,
        headers=headers,
        grade_id=grade_offerings[0].id,
    )

    assert r.status_code == 200, f"Expected 200, got {r.status_code}. Response: {r.text}"
    GradeSetupSchema.model_validate(r.json())
