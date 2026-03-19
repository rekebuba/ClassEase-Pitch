import random
from typing import Dict, List

from httpx import AsyncClient

from project.core.config import settings
from project.schema.models import (
    StreamSchema,
    YearSchema,
)
from project.schema.models.stream_schema import StreamWithRelatedSchema


class TestStreamsApi:
    async def test_get_streams(
        self,
        client: AsyncClient,
        admin_token_headers: Dict[str, str],
        year: YearSchema,
    ) -> None:
        """Test retrieving all streams."""
        r = await client.get(
            f"{settings.API_V1_STR}/streams",
            params={"yearId": str(year.id)},
            headers=admin_token_headers,
        )

        assert r.status_code == 200

    async def test_get_stream_by_id(
        self,
        client: AsyncClient,
        admin_token_headers: Dict[str, str],
        year: YearSchema,
        stream_relation: StreamWithRelatedSchema,
    ) -> None:
        """Test the API endpoint for retrieving a single stream by ID"""

        r = await client.get(
            f"{settings.API_V1_STR}/streams/{stream_relation.id}",
            params={"yearId": str(year.id)},
            headers=admin_token_headers,
        )

        assert r.status_code == 200

    async def test_get_stream_by_id_unauthorized(
        self,
        client: AsyncClient,
        year: YearSchema,
        stream_relation: StreamWithRelatedSchema,
    ) -> None:
        """Test that a 401 error is returned when no auth header is provided."""

        r = await client.get(
            f"{settings.API_V1_STR}/streams/{stream_relation.id}",
            params={"yearId": str(year.id)},
        )

        assert r.status_code == 401

    async def test_stream_unauthorized(
        self,
        client: AsyncClient,
        year: YearSchema,
    ) -> None:
        """Test retrieving all streams."""
        r = await client.get(
            f"{settings.API_V1_STR}/streams",
            params={"yearId": str(year.id)},
        )

        assert r.status_code == 401

    async def test_stream_relation(
        self,
        client: AsyncClient,
        admin_token_headers: Dict[str, str],
        streams: List[StreamSchema],
    ) -> None:
        """Test retrieving a stream with all its relationships."""
        stream = random.choice(streams)

        r = await client.get(
            f"{settings.API_V1_STR}/streams/{stream.id}/relation",
            headers=admin_token_headers,
        )

        assert r.status_code == 200
