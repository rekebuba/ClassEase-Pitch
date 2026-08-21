import random
import uuid
from typing import Awaitable, Callable

import pytest
import pytest_asyncio
from httpx import AsyncClient

from project.schema.models import SectionSchema
from project.schema.models.grade_stream_schema import GradeStreamSchema
from project.schema.schema import SuccessResponse
from tests.factories.api_data import (
    EnrollStudentApplicationFactory,
    SubmitEnrollmentApplicationFactory,
)
from tests.utils.api import API
from tests.utils.type_test import (
    MockSchool,
    MockSignUp,
    MockStudentProfile,
    SchoolAdmin,
    SchoolGrade,
    SchoolHR,
    SchoolStudent,
    SchoolUsers,
    UserScenario,
)


@pytest_asyncio.fixture(scope="session")
async def enroll_student(
    client: AsyncClient,
    schools: list[MockSchool],
    grades: dict[uuid.UUID, SchoolGrade],
    school_users: list[SchoolUsers],
    school_admins: dict[uuid.UUID, SchoolAdmin],
    get_sections: Callable[[dict[str, str], uuid.UUID], Awaitable[list[SectionSchema]]],
) -> Callable[[MockSchool, MockSignUp, GradeStreamSchema, uuid.UUID], Awaitable[UserScenario]]:
    """
    A factory fixture that returns a function to build the scenario.
    """

    async def _build(
        school: MockSchool,
        user: MockSignUp,
        grade_stream: GradeStreamSchema,
        application_id: uuid.UUID,
    ) -> UserScenario:
        school_id = school.response.school_id

        admin = school_admins[school_id].admins[0]

        sections = await get_sections(admin.login.headers, grade_stream.grade.id)
        section_ids = [section.id for section in sections]

        student_to_enroll = EnrollStudentApplicationFactory.create(
            application_id=application_id,
            section_id=random.choice(section_ids),
        )

        response = await API.post_student_enrollment(
            client=client,
            enrollment_data=student_to_enroll,
            headers=admin.login.headers,
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
        student_data = SuccessResponse.model_validate(response.json())
        assert student_data is not None, "Failed to validate response JSON"

        login_data = await API.login(
            client,
            username=user.request.username,
            password=user.request.password,
            school_slug=None,
        )

        user_info = await API.get_logged_in_user(
            client,
            headers=login_data.headers,
        )

        return UserScenario(
            school=school,
            signup=user,
            user_info=user_info,
            student=MockStudentProfile(
                request=student_to_enroll,
                response=student_data,
            ),
            login=login_data,
        )

    return _build


@pytest_asyncio.fixture(scope="session")
async def school_students(
    client: AsyncClient,
    school_users: list[SchoolUsers],
    school_hr_data: dict[uuid.UUID, SchoolHR],
    enroll_student: Callable[
        [MockSchool, MockSignUp, GradeStreamSchema, uuid.UUID],
        Awaitable[UserScenario],
    ],
) -> dict[uuid.UUID, SchoolStudent]:
    """Hire students for each school and return a map keyed by school_id."""

    students_by_school: dict[uuid.UUID, SchoolStudent] = {}

    for school_users_data in school_users:
        school = school_users_data.school
        school_id = school.response.school_id

        school_hr = school_hr_data.get(school_id)
        if not school_hr:
            raise KeyError(f"No HR data setup for school_id={school_id}")

        enrolled_students: list[UserScenario] = []

        assert len(school_users_data.students) <= len(school_hr.enrollment_opportunities), (
            f"Not enough enrollment_opportunities for school {school_id}: "
            f"{len(school_users_data.students)} students, "
            f"{len(school_hr.enrollment_opportunities)} enrollment_opportunities"
        )

        # Iterate directly over matched enrollment_opportunities for this specific school
        for student, opportunity in zip(school_users_data.students, school_hr.enrollment_opportunities):
            login = await API.login(
                client,
                username=student.request.username,
                password=student.request.password,
                school_slug=None,
            )

            enrollment_application = SubmitEnrollmentApplicationFactory.create(
                opportunity_id=opportunity.id,
                student_user_id=student.response.id,
            )

            # submit the enrollment application
            r = await API.post_enrollment_application(
                client=client,
                application_data=enrollment_application,
                headers=login.headers,
            )
            assert r.status_code == 201, f"Expected 201, got {r.status_code}. Response: {r.text}"
            application = SuccessResponse.model_validate(r.json())

            hired_student = await enroll_student(
                school,
                student,
                opportunity.grade_stream,
                application.id,
            )

            enrolled_students.append(hired_student)

        students_by_school[school_id] = SchoolStudent(
            school=school,
            students=enrolled_students,
        )

    return students_by_school


@pytest_asyncio.fixture
async def student(
    request: pytest.FixtureRequest,
    schools: list[MockSchool],
    school_students: dict[uuid.UUID, SchoolStudent],
) -> SchoolStudent:
    """Returns a single SchoolStudent for the parameterized school."""
    idx: int = request.param

    current_school = schools[idx]
    school_id = current_school.response.school_id

    school_student = school_students.get(school_id)
    if not school_student or not school_student.students:
        raise KeyError(f"No students found for school_id={school_id}")

    # Returns a single SchoolStudent
    return school_student
