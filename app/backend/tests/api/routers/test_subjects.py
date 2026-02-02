import random
from typing import Dict

from fastapi.testclient import TestClient

from project.core.config import settings
from project.models.year import Year


class TestSubjectsApi:
    def test_get_subjects(
        self,
        client: TestClient,
        admin_token_headers: Dict[str, str],
        year: Year,
    ) -> None:
        """Test retrieving all subjects."""
        r = client.get(
            f"{settings.API_V1_STR}/subjects",
            params={"yearId": str(year.id)},
            headers=admin_token_headers,
        )

        assert r.status_code == 200

    def test_get_subject_by_id(
        self,
        client: TestClient,
        admin_token_headers: Dict[str, str],
        year: Year,
    ) -> None:
        """Test the API endpoint for retrieving a single subject by ID"""
        subject = random.choice(year.subjects)
        r = client.get(
            f"{settings.API_V1_STR}/subjects/{subject.id}",
            params={"yearId": str(year.id)},
            headers=admin_token_headers,
        )

        assert r.status_code == 200

    def test_get_subject_by_id_unauthorized(
        self,
        client: TestClient,
        year: Year,
    ) -> None:
        """Test that a 401 error is returned when no auth header is provided."""
        subject = random.choice(year.subjects)
        r = client.get(
            f"{settings.API_V1_STR}/subjects/{subject.id}",
            params={"yearId": str(year.id)},
        )

        assert r.status_code == 401

    def test_subject_unauthorized(
        self,
        client: TestClient,
        year: Year,
    ) -> None:
        """Test retrieving all subjects."""
        r = client.get(
            f"{settings.API_V1_STR}/subjects",
            params={"yearId": str(year.id)},
        )

        assert r.status_code == 401
