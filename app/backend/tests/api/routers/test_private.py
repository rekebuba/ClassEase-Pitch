import pytest
from httpx import AsyncClient

from project.core.config import settings


@pytest.mark.parametrize(
    "token_fixture",
    [
        "admin_token_headers",
        # "teacher_token_headers",
        # "student_token_headers",
    ],
)
async def test_logged_in_user_info(
    client: AsyncClient,
    request: pytest.FixtureRequest,
    token_fixture: str,
) -> None:
    headers = request.getfixturevalue(token_fixture)
    r = await client.get(f"{settings.API_V1_STR}/me", headers=headers)

    assert r.status_code == 200


async def test_logged_in_user_info_unauthorized(client: AsyncClient) -> None:
    r = await client.get(f"{settings.API_V1_STR}/me")

    assert r.status_code == 401


async def test_logged_in_user_info_invalid_token(client: AsyncClient) -> None:
    headers = {"Authorization": "Bearer invalidtoken"}
    r = await client.get(f"{settings.API_V1_STR}/me", headers=headers)

    assert r.status_code == 401


async def test_logged_in_admin_info(
    client: AsyncClient, admin_token_headers: dict[str, str]
) -> None:
    r = await client.get(f"{settings.API_V1_STR}/me", headers=admin_token_headers)

    assert r.status_code == 200
