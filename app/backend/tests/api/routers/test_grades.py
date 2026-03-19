import random
from typing import Dict

from httpx import AsyncClient

from project.core.config import settings
from project.schema.models import YearSchema, YearWithRelatedSchema


class TestGradesApi:
    async def test_get_grades(
        self,
        client: AsyncClient,
        admin_token_headers: Dict[str, str],
        year: YearSchema,
    ) -> None:
        """Test retrieving all grades."""
        r = await client.get(
            f"{settings.API_V1_STR}/grades",
            params={"yearId": str(year.id)},
            headers=admin_token_headers,
        )

        assert r.status_code == 200

    async def test_get_grade_by_id(
        self,
        client: AsyncClient,
        admin_token_headers: Dict[str, str],
        year_relation: YearWithRelatedSchema,
    ) -> None:
        """Test the API endpoint for retrieving a single grade by ID"""
        grade = random.choice(year_relation.grades)
        r = await client.get(
            f"{settings.API_V1_STR}/grades/{grade.id}",
            params={"yearId": str(year_relation.id)},
            headers=admin_token_headers,
        )

        assert r.status_code == 200

    async def test_get_grade_by_id_unauthorized(
        self,
        client: AsyncClient,
        year_relation: YearWithRelatedSchema,
    ) -> None:
        """Test that a 401 error is returned when no auth header is provided."""
        grade = random.choice(year_relation.grades)
        r = await client.get(
            f"{settings.API_V1_STR}/grades/{grade.id}",
            params={"yearId": str(year_relation.id)},
        )

        assert r.status_code == 401

    async def test_grade_unauthorized(
        self,
        client: AsyncClient,
        year: YearSchema,
    ) -> None:
        """Test retrieving all grades."""
        r = await client.get(
            f"{settings.API_V1_STR}/grades",
            params={"yearId": str(year.id)},
        )

        assert r.status_code == 401

    async def test_grade_relation(
        self,
        client: AsyncClient,
        admin_token_headers: Dict[str, str],
        year_relation: YearWithRelatedSchema,
    ) -> None:
        """Test retrieving a grade with all its relationships."""
        grade = random.choice(year_relation.grades)

        r = await client.get(
            f"{settings.API_V1_STR}/grades/{grade.id}/relation",
            headers=admin_token_headers,
        )

        assert r.status_code == 200
