import random
from typing import Dict, List

from httpx import AsyncClient

from project.core.config import settings
from project.schema.models import (
    GradeWithRelatedSchema,
    SectionSchema,
    SectionWithRelatedSchema,
    YearWithRelatedSchema,
)


class TestSectionsApi:
    async def test_get_sections_unauthorized(
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
        )

        assert r.status_code == 401

    async def test_get_section_by_id(
        self,
        client: AsyncClient,
        admin_token_headers: Dict[str, str],
        sections: List[SectionSchema],
    ) -> None:
        """Test the API endpoint for retrieving a single section by ID"""
        section = random.choice(sections)

        r = await client.get(
            f"{settings.API_V1_STR}/sections/{section.id}",
            headers=admin_token_headers,
        )

        assert r.status_code == 200

    async def test_get_section_by_id_unauthorized(
        self,
        client: AsyncClient,
        sections: List[SectionSchema],
    ) -> None:
        """Test that a 401 error is returned when no auth header is provided."""
        section = random.choice(sections)

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

    async def test_get_section_relation(
        self,
        client: AsyncClient,
        admin_token_headers: Dict[str, str],
        sections: List[SectionSchema],
    ) -> None:
        """Test retrieving a section with its related data."""
        section = random.choice(sections)

        r = await client.get(
            f"{settings.API_V1_STR}/sections/{section.id}/relation",
            headers=admin_token_headers,
        )

        assert r.status_code == 200

        SectionWithRelatedSchema.model_validate_json(r.text)
