import uuid
from typing import Awaitable, Callable

import factory
import pytest
import pytest_asyncio
from httpx import AsyncClient

from project.api.v1.routers.departments.schema import DepartmentBase
from project.api.v1.routers.jobs.schema import JobPost
from project.api.v1.routers.positions.schema import PositionBase
from project.api.v1.routers.schema import FilterParams, SearchParams
from project.api.v1.routers.students.schema import EnrollmentOpportunityPost, EnrollmentOpportunitySchema
from project.schema.models import DepartmentSchema, PositionSchema
from project.schema.models.job_schema import JobSchema
from project.schema.schema import SuccessResponse
from tests.factories.api_data import EnrollmentOpportunityFactory, JobPostFactory, PositionFactory
from tests.utils.api import API
from tests.utils.type_test import MockSchool, SchoolAdmin, SchoolGrade, SchoolHR, SchoolUsers, SchoolYear


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
async def create_enrollment_opportunity(
    client: AsyncClient,
) -> Callable[[dict[str, str], EnrollmentOpportunityPost], Awaitable[SuccessResponse]]:
    async def _post_enrollment_opportunity(
        headers: dict[str, str], enrollment_opportunity: EnrollmentOpportunityPost
    ) -> SuccessResponse:
        r = await API.post_enrollment_opportunity(
            client=client,
            enrollment_opportunity=enrollment_opportunity,
            headers=headers,
        )
        assert r.status_code == 201, f"Expected 201, got {r.status_code}. Response: {r.text}"
        return SuccessResponse.model_validate(r.json())

    return _post_enrollment_opportunity


@pytest_asyncio.fixture(scope="session")
async def school_hr_data(
    client: AsyncClient,
    school_users: list[SchoolUsers],
    school_admins: dict[uuid.UUID, SchoolAdmin],
    years: dict[uuid.UUID, SchoolYear],
    grades: dict[uuid.UUID, SchoolGrade],
    create_department: Callable[[dict[str, str], DepartmentBase], Awaitable[SuccessResponse]],
    create_position: Callable[[dict[str, str], PositionBase], Awaitable[SuccessResponse]],
    create_job: Callable[[dict[str, str], JobPost], Awaitable[SuccessResponse]],
    create_enrollment_opportunity: Callable[[dict[str, str], EnrollmentOpportunityPost], Awaitable[SuccessResponse]],
) -> dict[uuid.UUID, SchoolHR]:
    school_hr: dict[uuid.UUID, SchoolHR] = {}

    for school in school_users:
        school_id = school.school.response.school_id

        admin = school_admins[school_id].admins[0]
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
            openings_count=2,
        )
        created_jobs = [await create_job(headers, job) for job in job_payloads]

        # Fetch jobs
        response = await API.get_school_jobs(
            client=client,
            headers=headers,
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"

        fetched_jobs = [JobSchema.model_validate(job) for job in response.json()]

        created_job_ids = {job.id for job in created_jobs}
        fetched_job_ids = {job.id for job in fetched_jobs}

        assert created_job_ids <= fetched_job_ids, "One or more newly created jobs were not found."

        enrollment_opportunity_payload = EnrollmentOpportunityFactory.create_batch(
            size=len(grades[school_id].grades),
            year_id=years[school_id].years[0].id,
            grade_id=factory.Iterator(grade.id for grade in grades[school_id].grades),
        )
        create_enrollment = [
            await create_enrollment_opportunity(headers, opportunity) for opportunity in enrollment_opportunity_payload
        ]

        # Fetch enrollment opportunities
        response = await API.get_enrollment_opportunities(
            client=client,
            headers=headers,
            query=FilterParams(year_id=years[school_id].years[0].id),
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"

        fetched_enrollment_opportunities = [
            EnrollmentOpportunitySchema.model_validate(opportunity) for opportunity in response.json()
        ]

        created_enrollment_ids = {opportunity.id for opportunity in create_enrollment}
        fetched_enrollment_ids = {opportunity.id for opportunity in fetched_enrollment_opportunities}

        assert created_enrollment_ids <= fetched_enrollment_ids, (
            "One or more newly created enrollment opportunities were not found."
        )

        school_hr[school.school.response.school_id] = SchoolHR(
            school=school.school,
            departments=fetched_departments,
            positions=fetched_positions,
            jobs=fetched_jobs,
            enrollment_opportunities=fetched_enrollment_opportunities,
        )

    return school_hr


@pytest_asyncio.fixture(scope="function")
async def school_HR(
    request: pytest.FixtureRequest,
    schools: list[MockSchool],
    school_hr_data: dict[uuid.UUID, SchoolHR],
) -> SchoolHR:
    idx = request.param

    # Defensive check: Ensure we are pulling data for the exact same school
    current_school = schools[idx]
    school_id = current_school.response.school_id

    return school_hr_data[school_id]
