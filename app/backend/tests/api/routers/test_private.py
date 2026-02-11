import pytest
from fastapi.testclient import TestClient

from project.core.config import settings


@pytest.mark.parametrize(
    "token_fixture",
    [
        "admin_token_headers",
        # "teacher_token_headers",
        # "student_token_headers",
    ],
)
def test_logged_in_user_info(
    client: TestClient, request: pytest.FixtureRequest, token_fixture: str
) -> None:
    headers = request.getfixturevalue(token_fixture)
    r = client.get(f"{settings.API_V1_STR}/me/", headers=headers)

    assert r.status_code == 200


def test_logged_in_user_info_unauthorized(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/me/")

    assert r.status_code == 401


def test_logged_in_user_info_invalid_token(client: TestClient) -> None:
    headers = {"Authorization": "Bearer invalidtoken"}
    r = client.get(f"{settings.API_V1_STR}/me/", headers=headers)

    assert r.status_code == 401


def test_logged_in_admin_info(
    client: TestClient, admin_token_headers: dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/me/", headers=admin_token_headers)

    assert r.status_code == 200
