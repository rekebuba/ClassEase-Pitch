from httpx import AsyncClient

from project.core.config import settings
from tests.utils.type_test import SchoolScenario


async def test_health_check(client: AsyncClient) -> None:
    r = await client.get(f"{settings.API_V1_STR}/health")
    assert r.status_code == 200


async def test_school_setup(school: SchoolScenario):
    pass
