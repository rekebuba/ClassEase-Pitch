import pytest
from httpx import AsyncClient

from project.api.v1.routers.schema import FilterParams
from project.api.v1.routers.subjects.schema import SubjectSetupSchema
from project.utils.enum import RoleEnum
from tests.utils.api import API
from tests.utils.type_test import SchoolScenario


@pytest.mark.parametrize(
    "role, search, expected_count",
    [
        (RoleEnum.ADMIN, None, 21),
        (RoleEnum.ADMIN, "None", 0),
        (RoleEnum.ADMIN, "Economics", 1),
        (RoleEnum.ADMIN, "", 21),
    ],
)
async def test_get_subjects_offerings(
    client: AsyncClient,
    school: SchoolScenario,
    role: RoleEnum,
    search: str | None,
    expected_count: int,
) -> None:
    """
    Test the get_subjects_offerings function for different user roles.
    """
    headers = school.find_user(lambda u: u.user_info.role == role).login.headers

    r = await API.get_subject_offerings(
        client=client,
        headers=headers,
        query=FilterParams(year_id=school.years.years[0].id, q=search),
    )
    assert r.status_code == 200, f"Expected 200, got {r.status_code}. Response: {r.text}"
    subject_offerings = [SubjectSetupSchema.model_validate(subject) for subject in r.json()]

    assert len(subject_offerings) == expected_count


@pytest.mark.parametrize(
    "role",
    [
        RoleEnum.ADMIN,
    ],
)
async def test_get_subject_offerings_by_id(client: AsyncClient, school: SchoolScenario, role: RoleEnum) -> None:
    """
    Test the get_subject_offerings_by_id function for different user roles.
    """
    headers = school.find_user(lambda u: u.user_info.role == role).login.headers

    r = await API.get_subject_offerings(
        client=client,
        headers=headers,
        query=FilterParams(year_id=school.years.years[0].id),
    )

    assert r.status_code == 200, f"Expected 200, got {r.status_code}. Response: {r.text}"
    subject_offerings = [SubjectSetupSchema.model_validate(subject) for subject in r.json()]

    assert len(subject_offerings) == 21

    r = await API.get_subject_offerings_by_id(
        client=client,
        headers=headers,
        subject_id=subject_offerings[0].id,
    )

    assert r.status_code == 200, f"Expected 200, got {r.status_code}. Response: {r.text}"
    SubjectSetupSchema.model_validate(r.json())
