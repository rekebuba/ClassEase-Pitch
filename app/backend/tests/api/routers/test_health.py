
from fastapi.testclient import TestClient
from project.core.config import settings


def test_health_check(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/health/")
    assert r.status_code == 200
