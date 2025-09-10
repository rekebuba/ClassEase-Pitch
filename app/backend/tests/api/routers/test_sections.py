import random
from typing import Dict

from fastapi.testclient import TestClient

from core.config import settings
from models.year import Year


class TestSectionsApi:
    def test_get_sections(
        self,
        client: TestClient,
        admin_token_headers: Dict[str, str],
        year: Year,
    ) -> None:
        """Test retrieving all sections."""
        grade = random.choice(year.grades)
        r = client.get(
            f"{settings.API_V1_STR}/sections",
            params={"gradeId": str(grade.id)},
            headers=admin_token_headers,
        )

        assert r.status_code == 200

    def test_get_section_by_id(
        self,
        client: TestClient,
        admin_token_headers: Dict[str, str],
        year: Year,
    ) -> None:
        """Test the API endpoint for retrieving a single section by ID"""
        grade = random.choice(year.grades)
        section = random.choice(grade.sections)

        r = client.get(
            f"{settings.API_V1_STR}/sections/{section.id}",
            headers=admin_token_headers,
        )

        assert r.status_code == 200

    def test_get_section_by_id_unauthorized(
        self,
        client: TestClient,
        year: Year,
    ) -> None:
        """Test that a 401 error is returned when no auth header is provided."""
        grade = random.choice(year.grades)
        section = random.choice(grade.sections)

        r = client.get(
            f"{settings.API_V1_STR}/sections/{section.id}",
        )

        assert r.status_code == 401

    def test_section_unauthorized(
        self,
        client: TestClient,
        year: Year,
    ) -> None:
        """Test retrieving all sections."""
        grade = random.choice(year.grades)
        r = client.get(
            f"{settings.API_V1_STR}/sections",
            params={"gradeId": str(grade.id)},
        )

        assert r.status_code == 401
