from collections.abc import AsyncGenerator

import pytest_asyncio
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from project.core.config import settings
from project.core.db import init_db, system_engine, tenant_engine
from project.models.base.base_model import Base


@pytest_asyncio.fixture(scope="session", loop_scope="session", autouse=True)
async def db() -> AsyncGenerator[None, None]:
    """Create tables once at the start and drop them at the end."""
    async with tenant_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed data that all tests need using a system session
    async with async_sessionmaker(system_engine, class_=AsyncSession)() as session:
        await init_db(system_session=session)

    yield

    # async with tenant_engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)

    # await tenant_engine.dispose()
    # await system_engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a fresh, transactional session for every single test"""

    async with tenant_engine.connect() as conn:
        """Start a transaction, yield a session, and rollback after the test."""
        trans = await conn.begin()

        async_session = async_sessionmaker(
            bind=conn,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        async with async_session() as session:
            yield session

        await trans.rollback()


@pytest_asyncio.fixture(scope="session")
async def system_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a fresh, transactional session for every single test"""

    async with system_engine.connect() as conn:
        """Start a transaction, yield a session, and rollback after the test."""
        trans = await conn.begin()

        async_session = async_sessionmaker(
            bind=conn,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        async with async_session() as session:
            yield session

        await trans.rollback()


@pytest_asyncio.fixture(scope="session")
async def test_redis():
    redis_client = Redis.from_url(str(settings.REDIS_URL), decode_responses=True)
    yield redis_client
    await redis_client.aclose()
