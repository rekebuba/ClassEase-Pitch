import random
from typing import Dict

from httpx import AsyncClient

from project.core.config import settings
from project.schema.models import YearSchema, YearWithRelatedSchema


class TestSubjectsApi:
    async def test_get_subjects(
        self,
        client: AsyncClient,
        admin_token_headers: Dict[str, str],
        year: YearSchema,
    ) -> None:
        """Test retrieving all subjects."""
        r = await client.get(
            f"{settings.API_V1_STR}/subjects",
            params={"yearId": str(year.id)},
            headers=admin_token_headers,
        )

        assert r.status_code == 200

    async def test_get_subject_by_id(
        self,
        client: AsyncClient,
        admin_token_headers: Dict[str, str],
        year: YearSchema,
        year_relation: YearWithRelatedSchema,
    ) -> None:
        """Test the API endpoint for retrieving a single subject by ID"""
        subject = random.choice(year_relation.subjects)
        r = await client.get(
            f"{settings.API_V1_STR}/subjects/{subject.id}",
            params={"yearId": str(year.id)},
            headers=admin_token_headers,
        )

        assert r.status_code == 200

    async def test_get_subject_by_id_unauthorized(
        self,
        client: AsyncClient,
        year: YearSchema,
        year_relation: YearWithRelatedSchema,
    ) -> None:
        """Test that a 401 error is returned when no auth header is provided."""
        subject = random.choice(year_relation.subjects)
        r = await client.get(
            f"{settings.API_V1_STR}/subjects/{subject.id}",
            params={"yearId": str(year.id)},
        )

        assert r.status_code == 401

    async def test_subject_unauthorized(
        self,
        client: AsyncClient,
        year: YearSchema,
    ) -> None:
        """Test retrieving all subjects."""
        r = await client.get(
            f"{settings.API_V1_STR}/subjects",
            params={"yearId": str(year.id)},
        )

        assert r.status_code == 401
