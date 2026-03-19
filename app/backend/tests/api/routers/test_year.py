from typing import Dict

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from project.api.v1.routers.year.schema import NewYearSuccess
from project.core.config import settings
from project.models.year import Year
from project.schema.models import YearSchema


class TestYearApi:
    async def test_new_academic_year(
        self,
        client: AsyncClient,
        admin_token_headers: Dict[str, str],
        db_session: AsyncSession,
        new_academic_year: NewYearSuccess,
    ) -> None:
        """Test creating a new academic year."""
        assert "Year created Successfully" == new_academic_year.message

        year = await db_session.get(Year, new_academic_year.id)
        assert year is not None

    async def test_get_years(
        self,
        client: AsyncClient,
        admin_token_headers: Dict[str, str],
    ) -> None:
        """Test retrieving all academic years."""

        r = await client.get(
            f"{settings.API_V1_STR}/years",
            headers=admin_token_headers,
        )

        assert r.status_code == 200

        years = r.json()
        assert isinstance(years, list)
        assert len(years) > 0

    async def test_year_relation(
        self,
        client: AsyncClient,
        admin_token_headers: Dict[str, str],
        year: YearSchema,
    ) -> None:
        """Test retrieving a year with all its relationships."""

        r = await client.get(
            f"{settings.API_V1_STR}/years/{year.id}/relation",
            headers=admin_token_headers,
        )

        assert r.status_code == 200
