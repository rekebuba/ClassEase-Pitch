import random
from typing import Dict

from fastapi.testclient import TestClient

from core.config import settings
from models.year import Year


class TestGradesApi:
    def test_get_grades(
        self,
        client: TestClient,
        admin_token_headers: Dict[str, str],
        year: Year,
    ) -> None:
        """Test retrieving all grades."""
        r = client.get(
            f"{settings.API_V1_STR}/grades",
            params={"yearId": str(year.id)},
            headers=admin_token_headers,
        )

        assert r.status_code == 200

    def test_get_grade_by_id(
        self,
        client: TestClient,
        admin_token_headers: Dict[str, str],
        year: Year,
    ) -> None:
        """Test the API endpoint for retrieving a single grade by ID"""
        grade = random.choice(year.grades)
        r = client.get(
            f"{settings.API_V1_STR}/grades/{grade.id}",
            params={"yearId": str(year.id)},
            headers=admin_token_headers,
        )

        assert r.status_code == 200

    def test_get_grade_by_id_unauthorized(
        self,
        client: TestClient,
        year: Year,
    ) -> None:
        """Test that a 401 error is returned when no auth header is provided."""
        grade = random.choice(year.grades)
        r = client.get(
            f"{settings.API_V1_STR}/grades/{grade.id}",
            params={"yearId": str(year.id)},
        )

        assert r.status_code == 401

    def test_grade_unauthorized(
        self,
        client: TestClient,
        year: Year,
    ) -> None:
        """Test retrieving all grades."""
        r = client.get(
            f"{settings.API_V1_STR}/grades",
            params={"yearId": str(year.id)},
        )

        assert r.status_code == 401
