import random
from typing import Dict

from httpx import AsyncClient

from project.core.config import settings
from project.schema.models import (
    GradeWithRelatedSchema,
    YearWithRelatedSchema,
)


class TestSectionsApi:
    async def test_get_sections(
        self,
        client: AsyncClient,
        admin_token_headers: Dict[str, str],
        year_relation: YearWithRelatedSchema,
    ) -> None:
        """Test retrieving all sections."""
        grade = random.choice(year_relation.grades)
        r = await client.get(
            f"{settings.API_V1_STR}/sections",
            params={"gradeId": str(grade.id)},
            headers=admin_token_headers,
        )

        assert r.status_code == 200

    async def test_get_section_by_id(
        self,
        client: AsyncClient,
        admin_token_headers: Dict[str, str],
        grade_relation: GradeWithRelatedSchema,
    ) -> None:
        """Test the API endpoint for retrieving a single section by ID"""
        section = random.choice(grade_relation.sections)

        r = await client.get(
            f"{settings.API_V1_STR}/sections/{section.id}",
            headers=admin_token_headers,
        )

        assert r.status_code == 200

    async def test_get_section_by_id_unauthorized(
        self,
        client: AsyncClient,
        grade_relation: GradeWithRelatedSchema,
    ) -> None:
        """Test that a 401 error is returned when no auth header is provided."""
        section = random.choice(grade_relation.sections)

        r = await client.get(
            f"{settings.API_V1_STR}/sections/{section.id}",
        )

        assert r.status_code == 401

    async def test_section_unauthorized(
        self,
        client: AsyncClient,
        grade_relation: GradeWithRelatedSchema,
    ) -> None:
        """Test retrieving all sections."""
        r = await client.get(
            f"{settings.API_V1_STR}/sections",
            params={"gradeId": str(grade_relation.id)},
        )

        assert r.status_code == 401
