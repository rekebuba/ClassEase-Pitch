import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from project.api.v1.routers.dependencies import get_db, get_redis
from project.main import app


@pytest_asyncio.fixture(scope="session")
async def client(db_session: AsyncSession, test_redis: Redis):
    """Setup client with dependency overrides."""

    app.dependency_overrides[get_db] = lambda: db_session
    app.dependency_overrides[get_redis] = lambda: test_redis

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
