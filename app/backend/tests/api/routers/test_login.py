from typing import Any

import jwt
import pytest
from httpx import AsyncClient
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from project.api.v1.routers.auth.schema import LoginTokenResponse, VerifyOTPResponse
from project.api.v1.routers.auth.service import (
    generate_and_store_otp_secret,
    generate_email_verification_token,
    verify_otp_and_generate_token,
)
from project.core.config import settings
from project.core.security import ALGORITHM
from project.models import (
    AuthSession,
    BlacklistToken,
)
from tests.utils.utils import _create_multi_school_user, _login


def _decode_access_token(access_token: str) -> dict[str, Any]:
    return jwt.decode(
        access_token,
        settings.SECRET_KEY.get_secret_value(),
        algorithms=[ALGORITHM],
    )


@pytest.mark.parametrize(
    "username,password",
    [
        (
            settings.FIRST_SUPERUSER,
            settings.FIRST_SUPERUSER_PASSWORD.get_secret_value(),
        ),
    ],
)
async def test_login(client: AsyncClient, username: str, password: str) -> None:
    login_data = {
        "username": username,
        "password": password,
    }
    r = await client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "accessToken" in tokens
    assert tokens["accessToken"]


async def test_student_login(client: AsyncClient, student_token_headers) -> None:
    pass


async def test_teacher_login(client: AsyncClient, teacher_token_headers) -> None:
    pass


async def test_login_incorrect_password(client: AsyncClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": "incorrect",
    }
    r = await client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert r.status_code == 400


async def test_login_non_existent_user(client: AsyncClient) -> None:
    login_data = {
        "username": "nonexistent",
        "password": "password",
    }
    r = await client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert r.status_code == 400


async def test_login_missing_fields(client: AsyncClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
    }
    r = await client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert r.status_code == 422


async def test_login_empty_fields(client: AsyncClient) -> None:
    login_data = {
        "username": "",
        "password": "",
    }
    r = await client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert r.status_code == 422


async def test_login_sql_injection_attempt(client: AsyncClient) -> None:
    login_data = {
        "username": "' OR '1'='1",
        "password": "' OR '1'='1",
    }
    r = await client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert r.status_code == 400


async def test_login_long_input(client: AsyncClient) -> None:
    long_username = "a" * 256
    long_password = "a" * 256
    login_data = {
        "username": long_username,
        "password": long_password,
    }
    r = await client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert r.status_code == 400


async def test_refresh_token_rotates_and_invalidates_previous_token(
    client: AsyncClient,
) -> None:
    login_response = await _login(
        client,
        username=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD.get_secret_value(),
    )
    old_refresh_token = login_response.refresh_token
    assert old_refresh_token is not None

    refresh_response = await client.post(
        f"{settings.API_V1_STR}/auth/refresh",
        json={"refresh_token": old_refresh_token},
    )
    assert refresh_response.status_code == 200

    refreshed = LoginTokenResponse.model_validate_json(refresh_response.text)
    assert refreshed.refresh_token is not None
    assert refreshed.refresh_token != old_refresh_token
    assert refreshed.access_token != login_response.access_token

    stale_refresh_response = await client.post(
        f"{settings.API_V1_STR}/auth/refresh",
        json={"refresh_token": old_refresh_token},
    )
    assert stale_refresh_response.status_code == 401


async def test_logout_blacklists_token_and_revokes_session(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    login_response = await _login(
        client,
        username=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD.get_secret_value(),
    )

    decoded = _decode_access_token(login_response.access_token)
    token_jti = decoded["jti"]
    token_session_id = decoded["session_id"]

    logout_response = await client.post(
        f"{settings.API_V1_STR}/auth/logout",
        headers={"Authorization": f"Bearer {login_response.access_token}"},
    )
    assert logout_response.status_code == 200

    blacklisted = (
        await db_session.execute(
            select(BlacklistToken).where(BlacklistToken.jti == token_jti)
        )
    ).scalar_one_or_none()
    assert blacklisted is not None

    auth_session = await db_session.get(AuthSession, token_session_id)
    assert auth_session is not None
    assert auth_session.revoked_at is not None
    assert auth_session.revoke_reason == "logout"

    me_response = await client.get(
        f"{settings.API_V1_STR}/me",
        headers={"Authorization": f"Bearer {login_response.access_token}"},
    )
    assert me_response.status_code == 401

    refresh_response = await client.post(
        f"{settings.API_V1_STR}/auth/refresh",
        json={"refresh_token": login_response.refresh_token},
    )
    assert refresh_response.status_code == 401


async def test_email_verification(client: AsyncClient) -> None:
    """Test the email verification endpoint with a valid token."""

    token = generate_email_verification_token(settings.FIRST_SUPERUSER_EMAIL)

    r = await client.get(
        f"{settings.API_V1_STR}/auth/verify-email",
        params={"token": token},
    )
    assert r.status_code == 200


async def test_email_verification_invalid_token(client: AsyncClient) -> None:
    """Test the email verification endpoint with an invalid token."""

    invalid_token = "invalidtoken"

    r = await client.get(
        f"{settings.API_V1_STR}/auth/verify-email",
        params={"token": invalid_token},
    )
    assert r.status_code == 400


async def test_email_verification_expired_token(
    client: AsyncClient,
    monkeypatch: Any,
) -> None:
    """Test the email verification endpoint with an expired token."""
    token = generate_email_verification_token(settings.FIRST_SUPERUSER_EMAIL)

    monkeypatch.setattr(settings, "EMAIL_RESET_TOKEN_EXPIRE_HOURS", -1)
    r = await client.get(
        f"{settings.API_V1_STR}/auth/verify-email",
        params={"token": token},
    )
    assert r.status_code == 400


"""
Note: Mailtrap's free plan limitations on sending emails.
To run these tests, you would need to mock the email sending functionality or
upgrade your Mailtrap plan. https://mailtrap.io/billing/plans/testing
"""
#
# async def test_forgot_password(client: AsyncClient) -> None:
#     """Test the forgot password endpoint with a valid email."""

#     r = await client.post(
#         f"{settings.API_V1_STR}/auth/password-recovery/{
#             settings.FIRST_SUPERUSER_EMAIL}",
#     )
#     assert r.status_code == 200

#     # Valid! Delete the secret so it's a "One-Time"
#     await redis_client.delete(f"otp:{settings.FIRST_SUPERUSER_EMAIL}")


async def test_forgot_password_non_existent_email(client: AsyncClient) -> None:
    """Test the forgot password endpoint with a non-existent email."""

    r = await client.post(
        f"{settings.API_V1_STR}/auth/password-recovery",
        json={"email": "nonexistent@example.com"},
    )
    assert r.status_code == 404


async def test_forgot_password_invalid_email_format(client: AsyncClient) -> None:
    """Test the forgot password endpoint with an invalid email format."""

    r = await client.post(
        f"{settings.API_V1_STR}/auth/password-recovery",
        json={"email": "invalid-email-format"},
    )
    assert r.status_code == 422


async def test_forgot_password_empty_email(client: AsyncClient) -> None:
    """Test the forgot password endpoint with an empty email."""

    r = await client.post(
        f"{settings.API_V1_STR}/auth/password-recovery",
        json={"email": ""},
    )
    assert r.status_code == 422


async def test_verify_otp(client: AsyncClient, test_redis: Redis) -> None:
    """Test the OTP verification endpoint with a valid OTP."""
    otp = await generate_and_store_otp_secret(
        settings.FIRST_SUPERUSER_EMAIL, test_redis
    )

    otp_data = {
        "email": settings.FIRST_SUPERUSER_EMAIL,
        "otp": otp,
    }
    r = await client.post(
        f"{settings.API_V1_STR}/auth/verify-otp",
        json=otp_data,
    )

    assert r.status_code == 200
    result = VerifyOTPResponse.model_validate_json(r.text)
    assert result.message == "OTP verified successfully"


async def test_verify_otp_invalid_code(client: AsyncClient) -> None:
    """Test the OTP verification endpoint with an invalid OTP."""
    otp_data = {
        "email": settings.FIRST_SUPERUSER_EMAIL,
        "otp": "invalidotp",
    }
    r = await client.post(f"{settings.API_V1_STR}/auth/verify-otp", json=otp_data)
    assert r.status_code == 400


async def test_verify_otp_invalid_email(client: AsyncClient) -> None:
    """Test the OTP verification endpoint with an invalid email."""
    otp_data = {
        "email": "invalid-email",
        "otp": "123456",
    }
    r = await client.post(f"{settings.API_V1_STR}/auth/verify-otp", json=otp_data)
    assert r.status_code == 422


async def test_password_reset(
    client: AsyncClient,
    db_session: AsyncSession,
    test_redis: Redis,
) -> None:
    """Test the password reset endpoint with valid data."""

    recovery_password = "InitialPassword123!"
    recovery_user = await _create_multi_school_user(
        db_session,
        password=recovery_password,
    )

    # First, generate a valid OTP and token for the test user
    otp = await generate_and_store_otp_secret(
        recovery_user["email"],
        test_redis,
    )
    token = await verify_otp_and_generate_token(
        email=recovery_user["email"],
        redis_client=test_redis,
        user_submitted_code=otp,
    )

    reset_data = {
        "email": recovery_user["email"],
        "token": token,
        "newPassword": "NewSecurePassword123!",
        "confirmPassword": "NewSecurePassword123!",
    }
    r = await client.post(f"{settings.API_V1_STR}/auth/password-reset", json=reset_data)
    assert r.status_code == 200

    # login with the new password to confirm it was changed successfully
    login_response = await _login(
        client,
        username=recovery_user["username"],
        password="NewSecurePassword123!",
        school_slug=recovery_user["primary_school_slug"],
    )

    assert login_response.access_token is not None
    assert login_response.token_type == "bearer"


async def test_password_reset_invalid_token(client: AsyncClient) -> None:
    """Test the password reset endpoint with an invalid token."""

    reset_data = {
        "email": settings.FIRST_SUPERUSER_EMAIL,
        "token": "invalidtoken",
        "newPassword": "NewSecurePassword123!",
        "confirmPassword": "NewSecurePassword123!",
    }
    r = await client.post(f"{settings.API_V1_STR}/auth/password-reset", json=reset_data)
    assert r.status_code == 400


async def test_login_requires_school_context_for_multi_membership_user(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    credentials = await _create_multi_school_user(
        db_session,
        password="MultiSchoolPass123!",
    )

    ambiguous_login_response = await client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": credentials["username"],
            "password": credentials["password"],
        },
    )
    assert ambiguous_login_response.status_code == 400
    assert "Multiple school memberships" in ambiguous_login_response.text

    scoped_login_response = await client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": credentials["username"],
            "password": credentials["password"],
            "schoolSlug": credentials["secondary_school_slug"],
        },
    )
    assert scoped_login_response.status_code == 200

    scoped_payload = LoginTokenResponse.model_validate_json(scoped_login_response.text)
    assert scoped_payload.active_school is not None
    assert scoped_payload.active_school.slug == credentials["secondary_school_slug"]
    assert scoped_payload.active_membership is not None
    assert (
        str(scoped_payload.active_membership.id)
        == credentials["secondary_membership_id"]
    )


async def test_login_supports_school_slug_prefixed_identifier(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    credentials = await _create_multi_school_user(
        db_session,
        password="PrefixedLogin123!",
    )

    prefixed_login = await client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": f"{credentials['secondary_school_slug']}:{credentials['username']}",  # noqa: E501
            "password": credentials["password"],
        },
    )
    assert prefixed_login.status_code == 200

    payload = LoginTokenResponse.model_validate_json(prefixed_login.text)
    assert payload.active_school is not None
    assert payload.active_school.slug == credentials["secondary_school_slug"]


async def test_select_membership_rotates_session_and_revokes_previous_credentials(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    credentials = await _create_multi_school_user(
        db_session,
        password="SwitchSchool123!",
    )

    initial_login = await _login(
        client,
        username=credentials["username"],
        password=credentials["password"],
        school_slug=credentials["primary_school_slug"],
    )

    previous_token_payload = _decode_access_token(initial_login.access_token)
    previous_session_id = previous_token_payload["session_id"]

    switch_response = await client.post(
        f"{settings.API_V1_STR}/auth/select-membership",
        json={"membership_id": credentials["secondary_membership_id"]},
        headers={"Authorization": f"Bearer {initial_login.access_token}"},
    )
    assert switch_response.status_code == 200

    switched_login = LoginTokenResponse.model_validate_json(switch_response.text)
    assert switched_login.active_membership is not None
    assert (
        str(switched_login.active_membership.id)
        == credentials["secondary_membership_id"]
    )

    old_session = await db_session.get(AuthSession, previous_session_id)
    assert old_session is not None
    assert old_session.revoked_at is not None
    assert old_session.revoke_reason == "school_switch"

    old_token_denied = await client.get(
        f"{settings.API_V1_STR}/me",
        headers={"Authorization": f"Bearer {initial_login.access_token}"},
    )
    assert old_token_denied.status_code == 401

    old_refresh_denied = await client.post(
        f"{settings.API_V1_STR}/auth/refresh",
        json={"refresh_token": initial_login.refresh_token},
    )
    assert old_refresh_denied.status_code == 401

    new_token_allowed = await client.get(
        f"{settings.API_V1_STR}/me",
        headers={"Authorization": f"Bearer {switched_login.access_token}"},
    )
    assert new_token_allowed.status_code == 200

    new_token_payload = _decode_access_token(switched_login.access_token)
    assert new_token_payload["membership_id"] == credentials["secondary_membership_id"]
    assert new_token_payload["session_id"] != previous_session_id
