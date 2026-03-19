from httpx import AsyncClient

from project.core.config import settings


async def test_health_check(client: AsyncClient) -> None:
    r = await client.get(f"{settings.API_V1_STR}/health")
    assert r.status_code == 200
