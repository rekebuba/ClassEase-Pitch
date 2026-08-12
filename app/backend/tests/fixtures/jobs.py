from typing import Awaitable, Callable

import factory
import pytest
import pytest_asyncio
from httpx import AsyncClient

from project.api.v1.routers.departments.schema import DepartmentBase
from project.api.v1.routers.jobs.schema import JobPost
from project.api.v1.routers.positions.schema import PositionBase
from project.api.v1.routers.schema import SearchParams
from project.schema.models import DepartmentSchema, PositionSchema
from project.schema.models.job_schema import JobSchema
from project.schema.schema import SuccessResponse
from tests.factories.api_data import JobPostFactory, PositionFactory
from tests.utils.api import API
from tests.utils.type_test import SchoolAdmin, SchoolHR, SchoolUsers, SchoolYear
from tests.utils.utils import find_admin_in_school


@pytest_asyncio.fixture(scope="session")
async def create_department(
    client: AsyncClient,
) -> Callable[[dict[str, str], DepartmentBase], Awaitable[SuccessResponse]]:
    async def _post_department(headers: dict[str, str], department: DepartmentBase) -> SuccessResponse:
        r = await API.post_department(
            client=client,
            department=department,
            headers=headers,
        )
        assert r.status_code == 201, f"Expected 201, got {r.status_code}. Response: {r.text}"
        return SuccessResponse.model_validate(r.json())

    return _post_department


@pytest_asyncio.fixture(scope="session")
async def create_position(
    client: AsyncClient,
) -> Callable[[dict[str, str], PositionBase], Awaitable[SuccessResponse]]:
    async def _post_position(headers: dict[str, str], position: PositionBase) -> SuccessResponse:
        r = await API.post_position(
            client=client,
            position=position,
            headers=headers,
        )
        assert r.status_code == 201, f"Expected 201, got {r.status_code}. Response: {r.text}"
        return SuccessResponse.model_validate(r.json())

    return _post_position


@pytest_asyncio.fixture(scope="session")
async def create_job(
    client: AsyncClient,
) -> Callable[[dict[str, str], JobPost], Awaitable[SuccessResponse]]:
    async def _post_job(headers: dict[str, str], job: JobPost) -> SuccessResponse:
        r = await API.post_job(
            client=client,
            job=job,
            headers=headers,
        )
        assert r.status_code == 201, f"Expected 201, got {r.status_code}. Response: {r.text}"
        return SuccessResponse.model_validate(r.json())

    return _post_job


@pytest_asyncio.fixture(scope="session")
async def school_hr_data(
    client: AsyncClient,
    school_users: list[SchoolUsers],
    admin_membership: list[SchoolAdmin],
    years: list[SchoolYear],
    create_department: Callable[[dict[str, str], DepartmentBase], Awaitable[SuccessResponse]],
    create_position: Callable[[dict[str, str], PositionBase], Awaitable[SuccessResponse]],
    create_job: Callable[[dict[str, str], JobPost], Awaitable[SuccessResponse]],
) -> list[SchoolHR]:
    school_hr: list[SchoolHR] = []

    for school in school_users:
        school_id = school.school.response.school_id

        admin = find_admin_in_school(
            admin_membership=admin_membership,
            school_id=school_id,
        )

        if admin is None:
            raise ValueError(f"No admin membership found for school with ID {school_id}")

        headers = admin.login.headers

        # Fetch departments
        response = await API.get_departments(
            client=client,
            headers=headers,
            query=SearchParams(q="Academic Affairs"),
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"

        fetched_departments = [DepartmentSchema.model_validate(department) for department in response.json()]
        assert len(fetched_departments) == 1, f"Expected 1 department, got {len(fetched_departments)}"
        assert fetched_departments[0].name == "Academic Affairs", (
            f"Expected department name 'Academic Affairs', got '{fetched_departments[0].name}'"
        )

        # Create positions
        position_payloads = PositionFactory.create_batch(
            size=3,
            title=factory.Iterator(["Maths Teacher", "Biology Teacher", "English Teacher"]),
            department_id=fetched_departments[0].id,
        )

        created_positions = [await create_position(headers, position) for position in position_payloads]

        # Fetch positions
        response = await API.get_positions(
            client=client,
            headers=headers,
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"

        fetched_positions = [PositionSchema.model_validate(position) for position in response.json()]

        created_position_ids = {position.id for position in created_positions}
        fetched_position_ids = {position.id for position in fetched_positions}

        assert created_position_ids <= fetched_position_ids, "One or more newly created positions were not found."

        # Create jobs
        job_payloads = JobPostFactory.create_batch(
            size=3,
            position_id=factory.Iterator([position.id for position in created_positions]),
        )
        created_jobs = [await create_job(headers, job) for job in job_payloads]

        # Fetch jobs
        response = await API.get_all_jobs(
            client=client,
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"

        fetched_jobs = [JobSchema.model_validate(job) for job in response.json()]

        created_job_ids = {job.id for job in created_jobs}
        fetched_job_ids = {job.id for job in fetched_jobs}

        assert created_job_ids <= fetched_job_ids, "One or more newly created jobs were not found."

        school_hr.append(
            SchoolHR(
                school=school.school,
                departments=fetched_departments,
                positions=fetched_positions,
                jobs=fetched_jobs,
            )
        )

    return school_hr


@pytest_asyncio.fixture(scope="function")
async def school_HR(
    request: pytest.FixtureRequest,
    school_hr_data: list[SchoolHR],
) -> SchoolHR:
    idx = request.param

    # Defensive check: Ensure we are pulling data for the exact same school
    current_school = school_hr_data[idx].school
    assert school_hr_data[idx].school == current_school

    return school_hr_data[idx]
