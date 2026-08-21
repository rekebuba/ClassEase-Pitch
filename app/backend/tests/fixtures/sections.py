import uuid
from typing import Awaitable, Callable

import pytest_asyncio
from httpx import AsyncClient

from project.api.v1.routers.sections.schema import SectionFilterParams
from project.schema.models import SectionSchema
from tests.utils.api import API


@pytest_asyncio.fixture(scope="session")
async def get_sections(
    client: AsyncClient,
) -> Callable[[dict[str, str], uuid.UUID], Awaitable[list[SectionSchema]]]:
    async def _get_section(headers: dict[str, str], grade_id: uuid.UUID) -> list[SectionSchema]:
        r = await API.get_sections(
            client=client,
            query=SectionFilterParams(grade_id=grade_id),
            headers=headers,
        )

        assert r.status_code == 200, f"Expected 200, got {r.status_code}. Response: {r.text}"
        return [SectionSchema.model_validate(section) for section in r.json()]

    return _get_section
