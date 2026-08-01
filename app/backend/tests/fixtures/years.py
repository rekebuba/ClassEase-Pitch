from typing import Awaitable, Callable

import pytest
import pytest_asyncio

from tests.fixtures import YEARS_PER_SCHOOL
from tests.utils.type_test import (
    MockSchool,
    MockSignUp,
    SchoolUsers,
    SchoolYear,
    YearScenario,
)


@pytest_asyncio.fixture(scope="session")
async def years(
    school_users: list[SchoolUsers],
    default_school_setup: Callable[[MockSchool, MockSignUp], Awaitable[YearScenario]],
) -> list[SchoolYear]:
    school: list[SchoolYear] = []

    for users in school_users:
        years: list[YearScenario] = []

        for _ in range(YEARS_PER_SCHOOL):
            year = await default_school_setup(users.school, users.admins[0])
            years.append(year)

        school.append(SchoolYear(school=users.school, years=years))

    return school


@pytest_asyncio.fixture
async def year(
    request: pytest.FixtureRequest,
    years: list[YearScenario],
) -> YearScenario:
    return years[request.param]
