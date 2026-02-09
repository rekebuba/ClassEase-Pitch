from fastapi.testclient import TestClient

from project.api.v1.routers.auth.service import generate_email_verification_token
from project.core.config import settings


def test_login(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD.get_secret_value(),
    }
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "accessToken" in tokens
    assert tokens["accessToken"]


def test_login_incorrect_password(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": "incorrect",
    }
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert r.status_code == 400


def test_login_non_existent_user(client: TestClient) -> None:
    login_data = {
        "username": "nonexistent",
        "password": "password",
    }
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert r.status_code == 400


def test_login_missing_fields(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
    }
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert r.status_code == 422


def test_login_empty_fields(client: TestClient) -> None:
    login_data = {
        "username": "",
        "password": "",
    }
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert r.status_code == 422


def test_login_sql_injection_attempt(client: TestClient) -> None:
    login_data = {
        "username": "' OR '1'='1",
        "password": "' OR '1'='1",
    }
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert r.status_code == 400


def test_login_long_input(client: TestClient) -> None:
    long_username = "a" * 256
    long_password = "a" * 256
    login_data = {
        "username": long_username,
        "password": long_password,
    }
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert r.status_code == 400


def test_email_verification(client: TestClient) -> None:
    """Test the email verification endpoint with a valid token."""

    token = generate_email_verification_token(settings.FIRST_SUPERUSER_EMAIL)

    r = client.get(
        f"{settings.API_V1_STR}/auth/verify-email",
        params={"token": token},
    )
    assert r.status_code == 200


def test_email_verification_invalid_token(client: TestClient) -> None:
    """Test the email verification endpoint with an invalid token."""

    invalid_token = "invalidtoken"

    r = client.get(
        f"{settings.API_V1_STR}/auth/verify-email",
        params={"token": invalid_token},
    )
    assert r.status_code == 400


def test_email_verification_expired_token(client: TestClient) -> None:
    """Test the email verification endpoint with an expired token."""

    pass
