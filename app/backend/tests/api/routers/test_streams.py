import random
from typing import Dict

from fastapi.testclient import TestClient

from core.config import settings
from models.year import Year


class TestStreamsApi:
    def test_get_streams(
        self,
        client: TestClient,
        admin_token_headers: Dict[str, str],
        year: Year,
    ) -> None:
        """Test retrieving all streams."""
        r = client.get(
            f"{settings.API_V1_STR}/streams",
            params={"yearId": str(year.id)},
            headers=admin_token_headers,
        )

        assert r.status_code == 200

    def test_get_stream_by_id(
        self,
        client: TestClient,
        admin_token_headers: Dict[str, str],
        year: Year,
    ) -> None:
        """Test the API endpoint for retrieving a single stream by ID"""
        grade = random.choice([grade for grade in year.grades if grade.has_stream])
        stream = random.choice(grade.streams)

        r = client.get(
            f"{settings.API_V1_STR}/streams/{stream.id}",
            params={"yearId": str(year.id)},
            headers=admin_token_headers,
        )

        assert r.status_code == 200

    def test_get_stream_by_id_unauthorized(
        self,
        client: TestClient,
        year: Year,
    ) -> None:
        """Test that a 401 error is returned when no auth header is provided."""
        grade = random.choice([grade for grade in year.grades if grade.has_stream])
        stream = random.choice(grade.streams)

        r = client.get(
            f"{settings.API_V1_STR}/streams/{stream.id}",
            params={"yearId": str(year.id)},
        )

        assert r.status_code == 401

    def test_stream_unauthorized(
        self,
        client: TestClient,
        year: Year,
    ) -> None:
        """Test retrieving all streams."""
        r = client.get(
            f"{settings.API_V1_STR}/streams",
            params={"yearId": str(year.id)},
        )

        assert r.status_code == 401
