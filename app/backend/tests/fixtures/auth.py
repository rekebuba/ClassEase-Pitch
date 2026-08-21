import pytest
from httpx import AsyncClient

from project.core.config import settings
from tests.utils.api import API
from tests.utils.type_test import (
    MockLogin,
)


@pytest.fixture(scope="session")
async def super_user(client: AsyncClient) -> MockLogin:
    return await API.login(
        client,
        username=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD.get_secret_value(),
        school_slug=None,
    )
