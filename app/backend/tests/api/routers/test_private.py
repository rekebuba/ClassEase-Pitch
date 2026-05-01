from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from project.core.config import settings
from project.utils.enum import (
    RoleEnum,
)
from tests.api.routers.test_login import _create_multi_school_user
from tests.utils.utils import _login_headers


def _assert_membership_summary_shape(membership: dict[str, Any]) -> None:
    required_keys = {
        "id",
        "schoolId",
        "schoolSlug",
        "schoolName",
        "status",
        "loginIdentifier",
        "isPrimary",
        "roleNames",
        "shellRole",
        "permissions",
    }
    assert required_keys.issubset(membership.keys())
    assert membership["roleNames"] == sorted(membership["roleNames"])
    assert membership["permissions"] == sorted(membership["permissions"])


def _assert_me_payload_shape(payload: dict[str, Any]) -> None:
    required_keys = {
        "id",
        "username",
        "role",
        "imagePath",
        "createdAt",
        "activeSchool",
        "activeMembership",
        "availableMemberships",
    }
    assert required_keys.issubset(payload.keys())

    active_school = payload["activeSchool"]
    assert {"id", "name", "slug", "status"}.issubset(active_school.keys())

    active_membership = payload["activeMembership"]
    _assert_membership_summary_shape(active_membership)

    available_memberships = payload["availableMemberships"]
    assert isinstance(available_memberships, list)
    assert len(available_memberships) >= 1
    for membership in available_memberships:
        _assert_membership_summary_shape(membership)


@pytest.fixture(scope="session")
async def multi_school_user(db_session: AsyncSession) -> dict[str, str]:
    return await _create_multi_school_user(db_session, password="MultiSchoolPass123!")


class TestPrivateRoutes:
    @pytest.mark.parametrize(
        "endpoint",
        [
            "/me",
            "/me/admin",
            "/me/teacher",
            "/me/student",
        ],
    )
    async def test_private_endpoints_require_auth(
        self,
        client: AsyncClient,
        endpoint: str,
    ) -> None:
        response = await client.get(f"{settings.API_V1_STR}{endpoint}")

        assert response.status_code == 401

    @pytest.mark.parametrize(
        "endpoint",
        [
            "/me",
            "/me/admin",
            "/me/teacher",
            "/me/student",
        ],
    )
    async def test_private_endpoints_reject_invalid_token(
        self,
        client: AsyncClient,
        endpoint: str,
    ) -> None:
        response = await client.get(
            f"{settings.API_V1_STR}{endpoint}",
            headers={"Authorization": "Bearer invalid-token"},
        )

        assert response.status_code == 401

    @pytest.mark.parametrize(
        ("token_headers", "expected_role"),
        [
            ("admin_token_headers", RoleEnum.ADMIN.value),
            ("teacher_token_headers", RoleEnum.TEACHER.value),
            ("student_token_headers", RoleEnum.STUDENT.value),
        ],
        indirect=["token_headers"],
    )
    async def test_me_returns_current_actor_payload(
        self,
        client: AsyncClient,
        request: pytest.FixtureRequest,
        token_headers: dict[str, str],
        expected_role: str,
    ) -> None:
        response = await client.get(f"{settings.API_V1_STR}/me", headers=token_headers)

        assert response.status_code == 200

        payload = response.json()
        _assert_me_payload_shape(payload)
        assert payload["role"] == expected_role

        active_membership_id = payload["activeMembership"]["id"]
        available_ids = {
            membership["id"] for membership in payload["availableMemberships"]
        }
        assert active_membership_id in available_ids

    async def test_me_admin_returns_admin_profile(
        self,
        client: AsyncClient,
        admin_token_headers: dict[str, str],
    ) -> None:
        response = await client.get(
            f"{settings.API_V1_STR}/me/admin",
            headers=admin_token_headers,
        )

        assert response.status_code == 200

        payload = response.json()
        _assert_me_payload_shape(payload)
        assert "admin" in payload
        assert payload["role"] == RoleEnum.ADMIN.value

    async def test_me_student_returns_student_profile(
        self,
        client: AsyncClient,
        student_token_headers: dict[str, str],
    ) -> None:
        response = await client.get(
            f"{settings.API_V1_STR}/me/student",
            headers=student_token_headers,
        )

        assert response.status_code == 200

        payload = response.json()
        _assert_me_payload_shape(payload)
        assert payload["role"] == RoleEnum.STUDENT.value
        assert "student" in payload
        assert payload["student"]["firstName"] == "Test"

    async def test_me_teacher_returns_response_validation_error_without_teacher_profile(
        self,
        client: AsyncClient,
        teacher_token_headers: dict[str, str],
    ) -> None:
        response = await client.get(
            f"{settings.API_V1_STR}/me/teacher",
            headers=teacher_token_headers,
        )

        assert response.status_code == 500
        assert response.json() == {
            "message": "Internal server error due to response validation failure."
        }

    async def test_me_admin_forbidden_for_teacher(
        self,
        client: AsyncClient,
        teacher_token_headers: dict[str, str],
    ) -> None:
        response = await client.get(
            f"{settings.API_V1_STR}/me/admin",
            headers=teacher_token_headers,
        )

        assert response.status_code == 403

    async def test_me_admin_forbidden_for_student(
        self,
        client: AsyncClient,
        student_token_headers: dict[str, str],
    ) -> None:
        response = await client.get(
            f"{settings.API_V1_STR}/me/admin",
            headers=student_token_headers,
        )

        assert response.status_code == 403

    async def test_me_student_forbidden_for_teacher(
        self,
        client: AsyncClient,
        teacher_token_headers: dict[str, str],
    ) -> None:
        response = await client.get(
            f"{settings.API_V1_STR}/me/student",
            headers=teacher_token_headers,
        )

        assert response.status_code == 403

    async def test_me_teacher_forbidden_for_student(
        self,
        client: AsyncClient,
        student_token_headers: dict[str, str],
    ) -> None:
        response = await client.get(
            f"{settings.API_V1_STR}/me/teacher",
            headers=student_token_headers,
        )

        assert response.status_code == 403

    async def test_me_supports_multi_school_memberships(
        self,
        client: AsyncClient,
        multi_school_user: dict[str, str],
    ) -> None:
        primary_headers = await _login_headers(
            client,
            username=multi_school_user["username"],
            password=multi_school_user["password"],
            school_slug=multi_school_user["primary_school_slug"],
        )
        secondary_headers = await _login_headers(
            client,
            username=multi_school_user["username"],
            password=multi_school_user["password"],
            school_slug=multi_school_user["secondary_school_slug"],
        )

        primary_response = await client.get(
            f"{settings.API_V1_STR}/me",
            headers=primary_headers,
        )
        secondary_response = await client.get(
            f"{settings.API_V1_STR}/me",
            headers=secondary_headers,
        )

        assert primary_response.status_code == 200
        assert secondary_response.status_code == 200

        primary_payload = primary_response.json()
        secondary_payload = secondary_response.json()

        assert (
            primary_payload["activeSchool"]["slug"]
            == multi_school_user["primary_school_slug"]
        )
        assert (
            secondary_payload["activeSchool"]["slug"]
            == multi_school_user["secondary_school_slug"]
        )

        primary_slugs = {
            membership["schoolSlug"]
            for membership in primary_payload["availableMemberships"]
        }
        secondary_slugs = {
            membership["schoolSlug"]
            for membership in secondary_payload["availableMemberships"]
        }
        expected_slugs = {
            multi_school_user["primary_school_slug"],
            multi_school_user["secondary_school_slug"],
        }

        assert expected_slugs.issubset(primary_slugs)
        assert expected_slugs.issubset(secondary_slugs)
