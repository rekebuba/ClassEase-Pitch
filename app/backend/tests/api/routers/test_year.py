from typing import Dict

from fastapi.testclient import TestClient

from core.config import settings
from tests.factories.api_data import NewYearFactory


class TestYearApi:
    def test_create_new_academic_year(
        self, client: TestClient, admin_token_headers: Dict[str, str]
    ) -> None:
        data = NewYearFactory.create()
        data.setup_methods = "Default Template"

        r = client.post(
            f"{settings.API_V1_STR}/years",
            json=data.model_dump(mode="json", by_alias=True),
            headers=admin_token_headers,
        )

        assert r.status_code == 201
        assert r.json() is not None

        result = r.json()

        assert "id" in result
        assert "message" in result
        assert "Year created Successfully" == result["message"]
