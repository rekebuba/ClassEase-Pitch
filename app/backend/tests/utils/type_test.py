from dataclasses import dataclass, field
from typing import Callable

from project.api.v1.routers.auth.route import SchoolAwareOAuth2PasswordRequestForm
from project.api.v1.routers.auth.schema import (
    LoginTokenResponse,
    SignUpRequest,
)
from project.api.v1.routers.grades.schema import GradeSetupSchema
from project.api.v1.routers.jobs.schema import HireJobApplication
from project.api.v1.routers.school.schema import (
    NewSchool,
    NewSchoolMembership,
    SuccessNewSchoolMembership,
    SuccessSchoolResponse,
)
from project.api.v1.routers.students.schema import EnrollmentOpportunitySchema, EnrollStudentApplication
from project.api.v1.routers.subjects.schema import SubjectSetupSchema
from project.api.v1.routers.users.schema import (
    CurrentUserInfo,
)
from project.api.v1.routers.year.schema import NewYear
from project.schema.models import DepartmentSchema, GradeSchema, PositionSchema, YearSchema
from project.schema.models.job_schema import JobSchema
from project.schema.schema import SuccessResponse
from project.utils.enum import RoleEnum


@dataclass
class MockSchool:
    request: NewSchool
    response: SuccessSchoolResponse


@dataclass
class MockSignUp:
    request: SignUpRequest
    response: SuccessResponse


@dataclass
class SchoolUsers:
    school: MockSchool
    admins: list[MockSignUp]
    students: list[MockSignUp]
    employees: list[MockSignUp]


@dataclass
class MockLogin:
    request: SchoolAwareOAuth2PasswordRequestForm
    response: LoginTokenResponse
    headers: dict[str, str]


@dataclass
class MockSchoolMembership:
    request: NewSchoolMembership
    response: SuccessNewSchoolMembership


@dataclass
class MockEmployeeProfile:
    request: HireJobApplication
    response: SuccessResponse


@dataclass
class MockStudentProfile:
    request: EnrollStudentApplication
    response: SuccessResponse


@dataclass
class UserScenario:
    school: MockSchool
    signup: MockSignUp
    login: MockLogin
    user_info: CurrentUserInfo
    membership: MockSchoolMembership | None = None
    employee: MockEmployeeProfile | None = None
    student: MockStudentProfile | None = None

    @property
    def is_admin(self) -> bool:
        return self.membership is not None and self.membership.request.role == RoleEnum.ADMIN

    @property
    def is_employee(self) -> bool:
        return self.employee is not None

    @property
    def is_student(self) -> bool:
        return self.student is not None

    def __post_init__(self):
        if self.membership and self.school and self.membership.response.school_id != self.school.response.school_id:
            raise ValueError(
                "UserScenario context mismatch: \
                User does not belong to the provided SchoolScenario."
            )


@dataclass
class SchoolAdmin:
    school: MockSchool
    admins: list[UserScenario]


@dataclass
class MockYear:
    request: NewYear
    response: SuccessResponse


@dataclass
class SchoolStudent:
    school: MockSchool
    students: list[UserScenario]


@dataclass
class SchoolEmployee:
    school: MockSchool
    employees: list[UserScenario]


@dataclass
class MockGrade:
    response: list[GradeSchema]


@dataclass
class SchoolGrade:
    school: MockSchool
    grades: list[GradeSetupSchema]


@dataclass
class SchoolSubject:
    school: MockSchool
    subjects: list[SubjectSetupSchema]


@dataclass
class SchoolDepartment:
    school: MockSchool
    departments: list[DepartmentSchema]
    new_department: SuccessResponse | None = None


@dataclass
class SchoolPosition:
    school: MockSchool
    positions: list[PositionSchema]
    new_position: SuccessResponse | None = None


@dataclass
class SchoolJob:
    school: MockSchool
    jobs: list[JobSchema]


@dataclass
class SchoolHR:
    school: MockSchool
    departments: list[DepartmentSchema] = field(default_factory=list)
    positions: list[PositionSchema] = field(default_factory=list)
    jobs: list[JobSchema] = field(default_factory=list)
    enrollment_opportunities: list[EnrollmentOpportunitySchema] = field(default_factory=list)


@dataclass
class YearScenario:
    school: MockSchool
    year: list[YearSchema]


@dataclass
class SchoolYear:
    school: MockSchool
    years: list[YearSchema]


@dataclass
class SchoolScenario:
    school: MockSchool
    users: list[UserScenario]
    years: SchoolYear
    grades: SchoolGrade
    subjects: SchoolSubject
    hr: SchoolHR

    def find_user(self, predicate: Callable[[UserScenario], bool]) -> UserScenario:
        """Finds the first user matching a custom condition."""
        for user in self.users:
            if predicate(user):
                return user
        raise ValueError("No user found matching the criteria.")

    def filter_users(self, predicate: Callable[[UserScenario], bool]) -> list[UserScenario]:
        """Returns all users matching a custom condition."""
        return [u for u in self.users if predicate(u)]
