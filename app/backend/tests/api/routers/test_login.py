import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from redis.asyncio import Redis

from project.api.v1.routers.auth.schema import VerifyOTPResponse
from project.api.v1.routers.auth.service import (
    generate_and_store_otp_secret,
    generate_email_verification_token,
)
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


"""
Note: Mailtrap's free plan limitations on sending emails.
To run these tests, you would need to mock the email sending functionality or
upgrade your Mailtrap plan. https://mailtrap.io/billing/plans/testing
"""
# @pytest.mark.asyncio
# async def test_forgot_password(async_client: AsyncClient) -> None:
#     """Test the forgot password endpoint with a valid email."""

#     r = await async_client.post(
#         f"{settings.API_V1_STR}/auth/password-recovery/{
#             settings.FIRST_SUPERUSER_EMAIL}",
#     )
#     assert r.status_code == 200

#     # Valid! Delete the secret so it's a "One-Time"
#     await redis_client.delete(f"otp:{settings.FIRST_SUPERUSER_EMAIL}")


def test_forgot_password_non_existent_email(client: TestClient) -> None:
    """Test the forgot password endpoint with a non-existent email."""

    r = client.post(
        f"{settings.API_V1_STR}/auth/password-recovery",
        json={"email": "nonexistent@example.com"},
    )
    assert r.status_code == 404


def test_forgot_password_invalid_email_format(client: TestClient) -> None:
    """Test the forgot password endpoint with an invalid email format."""

    r = client.post(
        f"{settings.API_V1_STR}/auth/password-recovery",
        json={"email": "invalid-email-format"},
    )
    assert r.status_code == 422


def test_forgot_password_empty_email(client: TestClient) -> None:
    """Test the forgot password endpoint with an empty email."""

    r = client.post(
        f"{settings.API_V1_STR}/auth/password-recovery/",
        json={"email": ""},
    )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_verify_otp(async_client: AsyncClient, test_redis: Redis) -> None:
    """Test the OTP verification endpoint with a valid OTP."""
    otp = await generate_and_store_otp_secret(
        settings.FIRST_SUPERUSER_EMAIL, test_redis
    )

    otp_data = {
        "email": settings.FIRST_SUPERUSER_EMAIL,
        "otp": otp,
    }
    r = await async_client.post(
        f"{settings.API_V1_STR}/auth/verify-otp",
        json=otp_data,
    )

    assert r.status_code == 200
    result = VerifyOTPResponse.model_validate_json(r.text)
    assert result.message == "OTP verified successfully"


@pytest.mark.asyncio
async def test_verify_otp_invalid_code(async_client: AsyncClient) -> None:
    """Test the OTP verification endpoint with an invalid OTP."""
    otp_data = {
        "email": settings.FIRST_SUPERUSER_EMAIL,
        "otp": "invalidotp",
    }
    r = await async_client.post(f"{settings.API_V1_STR}/auth/verify-otp", json=otp_data)
    assert r.status_code == 400


def test_verify_otp_invalid_email(client: TestClient) -> None:
    """Test the OTP verification endpoint with an invalid email."""
    otp_data = {
        "email": "invalid-email",
        "otp": "123456",
    }
    r = client.post(f"{settings.API_V1_STR}/auth/verify-otp", json=otp_data)
    assert r.status_code == 422


"""
Note: In SQLAlchemy, the synchronous Session does not play well with asyncio
because it blocks the event loop. To test async endpoints that depend on the database,
you would need to migrate from the synchronous Session to
an asynchronous session (AsyncSession) and use an async test client.
"""

# @pytest.mark.asyncio
# async def test_password_reset(
#     async_client: AsyncClient,
#     db_session: Session,
#     reset_superuser_password,
#     test_redis: Redis,
# ) -> None:
#     """Test the password reset endpoint with valid data."""

#     # First, generate a valid OTP and token for the test user
#     otp = await generate_and_store_otp_secret(
#         settings.FIRST_SUPERUSER_EMAIL,
#         test_redis,
#     )
#     token = await verify_otp_and_generate_token(settings.FIRST_SUPERUSER_EMAIL, otp)

#     reset_data = {
#         "email": settings.FIRST_SUPERUSER_EMAIL,
#         "token": token,
#         "newPassword": "NewSecurePassword123!",
#     }
#     r = await async_client.post(
#         f"{settings.API_V1_STR}/auth/password-reset", json=reset_data
#     )
#     assert r.status_code == 200

#     # login with the new password to confirm it was changed successfully
#     login_data = {
#         "username": settings.FIRST_SUPERUSER,
#         "password": "NewSecurePassword123!",
#     }
#     r = await async_client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
#     assert r.status_code == 200

#     result = LoginTokenResponse.model_validate_json(r.text)
#     assert result.access_token is not None
#     assert result.token_type == "bearer"


@pytest.mark.asyncio
async def test_password_reset_invalid_token(client: TestClient) -> None:
    """Test the password reset endpoint with an invalid token."""

    # First, generate a valid OTP and token for the test user

    reset_data = {
        "email": settings.FIRST_SUPERUSER_EMAIL,
        "token": "invalidtoken",
        "newPassword": "NewSecurePassword123!",
        "confirmPassword": "NewSecurePassword123!",
    }
    r = client.post(f"{settings.API_V1_STR}/auth/password-reset", json=reset_data)
    assert r.status_code == 400
