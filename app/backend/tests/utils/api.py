import uuid

import httpx
from httpx import AsyncClient

from project.api.v1.routers.auth.schema import (
    LoginTokenResponse,
    SignUpRequest,
)
from project.api.v1.routers.departments.schema import DepartmentBase
from project.api.v1.routers.employee.schema import EmployeePositionCreate
from project.api.v1.routers.grades.schema import GradeSetupSchema
from project.api.v1.routers.jobs.schema import HireJobApplication, JobApplicationPost, JobPost
from project.api.v1.routers.positions.schema import PositionBase
from project.api.v1.routers.schema import FilterParams, SearchParams
from project.api.v1.routers.school.schema import EmployeeProfile
from project.api.v1.routers.subjects.schema import SubjectSetupSchema
from project.api.v1.routers.teachers.schema import CreateTeacherProfile
from project.api.v1.routers.users.schema import (
    CurrentUserInfo,
)
from project.api.v1.routers.year.schema import NewYear
from project.core.config import settings
from project.schema.models import GradeSchema, SectionSchema
from project.schema.schema import SuccessResponse
from tests.factories.api_data import LoginFactory
from tests.utils.type_test import (
    MockEmployeeProfile,
    MockLogin,
    MockSignUp,
    MockYear,
)


class API:
    @staticmethod
    async def signup(client: AsyncClient, user: SignUpRequest) -> MockSignUp:
        r = await client.post(
            f"{settings.API_V1_STR}/auth/signup",
            json=user.model_dump(mode="json"),
        )
        assert r.status_code == 201, f"Expected 201, got {r.status_code}. {r.text}"
        return MockSignUp(request=user, response=SuccessResponse.model_validate(r.json()))

    @staticmethod
    async def login(
        client: AsyncClient,
        *,
        username: str,
        password: str,
        school_slug: str | None = None,
    ) -> MockLogin:
        login_form = LoginFactory.create(
            username=username,
            password=password,
            school_slug=school_slug,
        )

        r = await client.post(
            f"{settings.API_V1_STR}/auth/login",
            data={
                "username": login_form.username,
                "password": login_form.password,
                "schoolSlug": login_form.school_slug,
            },
        )
        assert r.status_code == 200, f"Expected 200, got {r.status_code}. Response: {r.text}"

        response = LoginTokenResponse.model_validate(r.json())
        return MockLogin(
            request=login_form,
            response=response,
            headers={"Authorization": f"Bearer {response.access_token}"},
        )

    @staticmethod
    async def get_logged_in_user(
        client: AsyncClient,
        headers: dict[str, str],
    ) -> CurrentUserInfo:
        r = await client.get(
            f"{settings.API_V1_STR}/user",
            headers=headers,
        )
        assert r.status_code == 200, f"Expected 200, got {r.status_code}. Response: {r.text}"
        return CurrentUserInfo.model_validate(r.json())

    @staticmethod
    async def post_year(
        *,
        client: AsyncClient,
        new_year: NewYear,
        headers: dict[str, str],
    ) -> MockYear:
        r = await client.post(
            f"{settings.API_V1_STR}/years",
            json=new_year.model_dump(mode="json"),
            headers=headers,
        )
        assert r.status_code == 201, f"Expected 201, got {r.status_code}. Response: {r.text}"
        return MockYear(request=new_year, response=SuccessResponse.model_validate(r.json()))

    @staticmethod
    async def post_department(
        *,
        client: AsyncClient,
        department: DepartmentBase,
        headers: dict[str, str],
    ) -> httpx.Response:
        return await client.post(
            f"{settings.API_V1_STR}/departments",
            json=department.model_dump(mode="json"),
            headers=headers,
        )

    @staticmethod
    async def get_departments(
        *,
        client: AsyncClient,
        headers: dict[str, str],
        query: SearchParams | None = None,
    ) -> httpx.Response:
        return await client.get(
            f"{settings.API_V1_STR}/departments",
            headers=headers,
            params=query.model_dump() if query else None,
        )

    @staticmethod
    async def get_department(
        *,
        client: AsyncClient,
        headers: dict[str, str],
        department_id: uuid.UUID,
    ) -> httpx.Response:
        return await client.get(
            f"{settings.API_V1_STR}/departments/{department_id}",
            headers=headers,
        )

    @staticmethod
    async def post_position(
        *,
        client: AsyncClient,
        position: PositionBase,
        headers: dict[str, str],
    ) -> httpx.Response:
        return await client.post(
            f"{settings.API_V1_STR}/positions",
            json=position.model_dump(mode="json"),
            headers=headers,
        )

    @staticmethod
    async def get_positions(
        *,
        client: AsyncClient,
        headers: dict[str, str],
        query: SearchParams | None = None,
    ) -> httpx.Response:
        return await client.get(
            f"{settings.API_V1_STR}/positions",
            headers=headers,
            params=query.model_dump() if query else None,
        )

    @staticmethod
    async def get_position(
        *,
        client: AsyncClient,
        headers: dict[str, str],
        position_id: uuid.UUID,
    ) -> httpx.Response:
        return await client.get(
            f"{settings.API_V1_STR}/positions/{position_id}",
            headers=headers,
        )

    @staticmethod
    async def post_job(
        *,
        client: AsyncClient,
        job: JobPost,
        headers: dict[str, str],
    ) -> httpx.Response:
        return await client.post(
            f"{settings.API_V1_STR}/jobs",
            json=job.model_dump(mode="json"),
            headers=headers,
        )

    @staticmethod
    async def get_all_jobs(
        *,
        client: AsyncClient,
        query: SearchParams | None = None,
    ) -> httpx.Response:
        return await client.get(
            f"{settings.API_V1_STR}/jobs",
            params=query.model_dump() if query else None,
        )

    @staticmethod
    async def get_school_jobs(
        *,
        client: AsyncClient,
        headers: dict[str, str],
        query: SearchParams | None = None,
    ) -> httpx.Response:
        return await client.get(
            f"{settings.API_V1_STR}/school-jobs",
            headers=headers,
            params=query.model_dump() if query else None,
        )

    @staticmethod
    async def post_job_application(
        *,
        client: AsyncClient,
        job_id: uuid.UUID,
        application_data: JobApplicationPost,
        headers: dict[str, str],
    ) -> httpx.Response:
        return await client.post(
            f"{settings.API_V1_STR}/job-applications",
            json=application_data.model_dump(mode="json"),
            headers=headers,
        )

    @staticmethod
    async def get_job_applications(
        *,
        client: AsyncClient,
        headers: dict[str, str],
        query: SearchParams | None = None,
    ) -> httpx.Response:
        return await client.get(
            f"{settings.API_V1_STR}/job-applications",
            headers=headers,
            params=query.model_dump() if query else None,
        )

    @staticmethod
    async def hire_employee(
        *,
        client: AsyncClient,
        employee_data: HireJobApplication,
        headers: dict[str, str],
    ) -> httpx.Response:
        return await client.post(
            f"{settings.API_V1_STR}/job-applications/hire",
            json=employee_data.model_dump(mode="json"),
            headers=headers,
        )

    @staticmethod
    async def post_employee(
        *,
        client: AsyncClient,
        employee_profile: EmployeeProfile,
        headers: dict[str, str],
    ) -> MockEmployeeProfile:
        r = await client.post(
            f"{settings.API_V1_STR}/employees",
            json=employee_profile.model_dump(mode="json"),
            headers=headers,
        )
        assert r.status_code == 201, f"Expected 201, got {r.status_code}. Response: {r.text}"
        return MockEmployeeProfile(
            request=employee_profile,
            response=SuccessResponse.model_validate(r.json()),
        )

    @staticmethod
    async def post_employee_position(
        *,
        client: AsyncClient,
        employee_profile: EmployeePositionCreate,
        headers: dict[str, str],
    ) -> SuccessResponse:
        r = await client.post(
            f"{settings.API_V1_STR}/employee-positions",
            json=employee_profile.model_dump(mode="json"),
            headers=headers,
        )
        assert r.status_code == 201, f"Expected 201, got {r.status_code}. Response: {r.text}"
        return SuccessResponse.model_validate(r.json())

    @staticmethod
    async def post_teacher_profile(
        *,
        client: AsyncClient,
        teacher_profile: CreateTeacherProfile,
        headers: dict[str, str],
    ) -> SuccessResponse:
        r = await client.post(
            f"{settings.API_V1_STR}/teacher-profiles",
            json=teacher_profile.model_dump(mode="json"),
            headers=headers,
        )
        assert r.status_code == 201, f"Expected 201, got {r.status_code}. Response: {r.text}"
        return SuccessResponse.model_validate(r.json())

    @staticmethod
    async def get_grades(
        *,
        client: AsyncClient,
        headers: dict[str, str],
    ) -> list[GradeSchema]:
        r = await client.get(
            f"{settings.API_V1_STR}/grades",
            headers=headers,
        )
        assert r.status_code == 200, f"Expected 200, got {r.status_code}. Response: {r.text}"
        return [GradeSchema.model_validate(grade) for grade in r.json()]

    @staticmethod
    async def get_grades_offerings(
        *,
        client: AsyncClient,
        headers: dict[str, str],
        query: FilterParams,
    ) -> list[GradeSetupSchema]:
        r = await client.get(
            f"{settings.API_V1_STR}/grades/offerings",
            headers=headers,
            params=query.model_dump(),
        )
        assert r.status_code == 200, f"Expected 200, got {r.status_code}. Response: {r.text}"
        # print(json.dumps(r.json(), indent=4, sort_keys=True))
        return [GradeSetupSchema.model_validate(grade) for grade in r.json()]

    @staticmethod
    async def get_grade_offerings_by_id(
        *,
        client: AsyncClient,
        headers: dict[str, str],
        grade_id: uuid.UUID,
    ) -> GradeSetupSchema:
        r = await client.get(
            f"{settings.API_V1_STR}/grades/offerings/{grade_id}",
            headers=headers,
        )
        assert r.status_code == 200, f"Expected 200, got {r.status_code}. Response: {r.text}"
        return GradeSetupSchema.model_validate(r.json())

    @staticmethod
    async def get_subjects_offerings(
        *,
        client: AsyncClient,
        headers: dict[str, str],
        query: FilterParams,
    ) -> list[SubjectSetupSchema]:
        r = await client.get(
            f"{settings.API_V1_STR}/subjects/offerings",
            headers=headers,
            params=query.model_dump(),
        )
        assert r.status_code == 200, f"Expected 200, got {r.status_code}. Response: {r.text}"
        return [SubjectSetupSchema.model_validate(subject) for subject in r.json()]

    @staticmethod
    async def get_subject_offerings_by_id(
        *,
        client: AsyncClient,
        headers: dict[str, str],
        subject_id: uuid.UUID,
    ) -> SubjectSetupSchema:
        r = await client.get(
            f"{settings.API_V1_STR}/subjects/offerings/{subject_id}",
            headers=headers,
        )
        assert r.status_code == 200, f"Expected 200, got {r.status_code}. Response: {r.text}"
        return SubjectSetupSchema.model_validate(r.json())

    @staticmethod
    async def get_sections(
        *,
        client: AsyncClient,
        headers: dict[str, str],
        grade_id: uuid.UUID,
    ) -> list[SectionSchema]:
        r = await client.get(
            f"{settings.API_V1_STR}/sections?grade_id={grade_id}",
            headers=headers,
        )
        assert r.status_code == 200, f"Expected 200, got {r.status_code}. Response: {r.text}"
        return [SectionSchema.model_validate(section) for section in r.json()]
