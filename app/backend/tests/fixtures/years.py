import uuid

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from project.schema.models import YearSchema
from project.schema.schema import SuccessResponse
from project.utils.enum import AcademicYearStatusEnum
from tests.factories.api_data import NewYearFactory
from tests.utils.api import API
from tests.utils.type_test import (
    MockSchool,
    SchoolAdmin,
    SchoolYear,
)
from tests.utils.utils import _assert_provisioned_models_counts


@pytest_asyncio.fixture(scope="session")
async def years(
    client: AsyncClient,
    db_session: AsyncSession,
    schools: list[MockSchool],
    school_admins: dict[uuid.UUID, SchoolAdmin],
) -> dict[uuid.UUID, SchoolYear]:
    years_map: dict[uuid.UUID, SchoolYear] = {}

    for school in schools:
        school_id = school.response.school_id

        admin = school_admins[school_id].admins[0]

        new_year = NewYearFactory.create(
            setup_methods="Default Template",
            status=AcademicYearStatusEnum.ACTIVE,
        )
        admin.login.headers["x-school-slug"] = school.request.slug

        r = await API.post_year(
            client=client,
            new_year=new_year,
            headers=admin.login.headers,
        )
        assert r.status_code == 201, f"Expected 201, got {r.status_code}. Response: {r.text}"
        assert SuccessResponse.model_validate(r.json()) is not None, "Failed to create a new academic year."

        await _assert_provisioned_models_counts(
            tenant_session=db_session,
            school_id=school_id,
        )

        r = await API.get_years(
            client=client,
            headers=admin.login.headers,
        )

        assert r.status_code == 200, f"Expected 200, got {r.status_code}. Response: {r.text}"
        assert type(r.json()) is list, f"Expected a list of academic years, got {type(r.json())}"
        years = [YearSchema.model_validate(year) for year in r.json()]

        years_map[school_id] = SchoolYear(
            school=school,
            years=years,
        )

    return years_map


@pytest_asyncio.fixture
async def year(
    request: pytest.FixtureRequest,
    schools: list[MockSchool],
    years: dict[uuid.UUID, SchoolYear],
) -> SchoolYear:
    """Returns the active/latest YearScenario for the parameterized school."""
    idx: int = request.param

    current_school = schools[idx]
    school_id = current_school.response.school_id

    # Retrieve list of years for this school safely
    school_years = years.get(school_id)
    if not school_years:
        raise KeyError(f"No academic years found for school_id={school_id}")

    # Return a single YearScenario (the latest created year)
    return school_years
