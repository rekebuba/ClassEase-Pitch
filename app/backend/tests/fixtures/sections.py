import pytest_asyncio
from httpx import AsyncClient

from project.schema.models import GradeSchema
from tests.utils.api import API
from tests.utils.type_test import SchoolAdmin, SectionScenario


@pytest_asyncio.fixture(scope="session")
async def sections(
    client: AsyncClient,
    grades: list[GradeSchema],
    admin: SchoolAdmin,
) -> list[SectionScenario]:
    created: list[SectionScenario] = []

    for grade in grades:
        sections = await API.get_sections(
            client=client,
            headers=admin.login.headers,
            grade_id=grade.id,
        )

        created.append(SectionScenario(grade=grade, sections=sections))

    return created
