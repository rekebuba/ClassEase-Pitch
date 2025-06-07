from typing import Iterator, List, Dict, Any, Optional, Tuple
from pydantic import BaseModel
import pytest
from flask.testing import FlaskClient

from models.grade import Grade
from models.student import Student
from tests.test_api.factories import AssessmentFactory, SemesterFactory, StudentFactory
from tests.typing import Credential

from sqlalchemy import func
from sqlalchemy.orm import scoped_session, Session, Query

from models.subject import Subject


@pytest.fixture(scope="session")
def stud_course_register(
    client: FlaskClient, create_semester: None, all_stud_auth_header: List[Credential]
) -> None:
    for auth_header in all_stud_auth_header:
        get_course = client.get(
            "/api/v1/student/course/registration", headers=auth_header["header"]
        )
        assert get_course.status_code == 200
        courses = get_course.json

        response = client.post(
            "/api/v1/student/course/registration",
            json=courses,
            headers=auth_header["header"],
        )

        # Debugging failed cases
        if response.status_code != 201:
            print(f"Failed for: {courses}")
            print(f"Response: {response.json}")

        assert response.status_code == 201
        assert response.json is not None
        assert "message" in response.json
        assert response.json["message"] == "Course registration successful!"


# --- Pydantic Models for Response Validation ---
class ResponseData(BaseModel):
    """for all students data after post dump."""

    identification: str
    imagePath: str
    createdAt: str
    guardianName: str
    guardianPhone: str
    isActive: bool
    firstName_fatherName_grandFatherName: str
    grade: Optional[int]
    finalScore: Optional[float]
    rank: Optional[int]
    semesterOne: Optional[int]
    semesterTwo: Optional[int]
    sectionSemesterOne: Optional[str]
    sectionSemesterTwo: Optional[str]
    averageSemesterOne: Optional[float]
    averageSemesterTwo: Optional[float]
    rankSemesterOne: Optional[int]
    rankSemesterTwo: Optional[int]


class ResponseTableId(BaseModel):
    identification: str
    imagePath: str
    createdAt: str
    firstName_fatherName_grandFatherName: str
    guardianName: str
    guardianPhone: str
    isActive: str
    grade: str
    sectionSemesterOne: str
    sectionSemesterTwo: str
    averageSemesterOne: str
    averageSemesterTwo: str
    rankSemesterOne: str
    rankSemesterTwo: str
    semesterOne: str
    semesterTwo: str
    finalScore: str
    rank: str


class StudentQueryResponse(BaseModel):
    tableId: ResponseTableId
    data: List[ResponseData]


# --- Test Data Generation ---
@pytest.fixture(scope="module")
def student_data(db_session: scoped_session[Session]) -> Iterator[Student]:
    """Fixture to create test student data."""
    grade_ids = db_session.query(Grade.id).order_by(Grade.grade).all()
    for grade_id in grade_ids:
        # Create 10 students for each grade
        StudentFactory.create_batch(3, grade_id=grade_id[0])

    db_session.commit()

    yield db_session.query(Student).all()


@pytest.fixture(scope="module")
def all_subjects(
    db_session: scoped_session[Session],
) -> Iterator[Query[Tuple[int, int]]]:
    """Fixture to create and return available subjects."""
    query = (
        db_session.query(func.count().label("row_count"), Grade.grade)
        .select_from(Subject)
        .join(Grade, Subject.grade_id == Grade.id)
        .filter(Grade.grade <= 10)
        .group_by(Subject.grade_id)
        .order_by(Grade.grade)
    )
    yield query


@pytest.fixture(scope="module")
def register_all_students(
    db_session: scoped_session[Session],
    student_data: Iterator[Student],
    all_subjects: Query[Tuple[int, int]],
) -> None:
    """Fixture to register all students in the database."""
    for student in student_data:
        # For each student, create assessments based on the grade
        subjects_for_registration = all_subjects.filter(
            Grade.id == student.current_grade_id
        ).all()
        for row_count, grade in subjects_for_registration:
            # Reset the sequence counter
            AssessmentFactory.reset_sequence()
            AssessmentFactory.create_batch(row_count, student_id=student.id)


@pytest.fixture(scope="module")
def register_all_students_second_semester(
    db_session: scoped_session[Session],
    student_data: Iterator[Student],
    all_subjects: Query[Tuple[int, int]],
) -> None:
    """Fixture to register all students in the second semester."""
    second_semester = SemesterFactory.create(
        name=2
    )  # Create second semester (overrides default)
    for student in student_data:
        # For each student, create assessments based on the grade
        subjects_for_registration = all_subjects.filter(
            Grade.id == student.current_grade_id
        ).all()
        for row_count, grade in subjects_for_registration:
            # Reset the sequence counter
            AssessmentFactory.reset_sequence()
            AssessmentFactory.create_batch(
                row_count, student_id=student.id, semester_id=second_semester.id
            )


@pytest.fixture(scope="module")
def student_query_table_data(
    client: FlaskClient, admin_auth_header: Credential
) -> Iterator[StudentQueryResponse]:
    table_resp = client.post(
        "/api/v1/admin/students", json={}, headers=admin_auth_header["header"]
    )
    assert table_resp.status_code == 200
    assert table_resp.json is not None

    table_data = StudentQueryResponse(**table_resp.json)

    yield table_data
