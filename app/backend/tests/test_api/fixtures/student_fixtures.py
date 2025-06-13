from datetime import datetime
from typing import Iterator, List, Optional, Tuple
from pydantic import BaseModel
import pytest
from flask.testing import FlaskClient

from models.grade import Grade
from models.semester import Semester
from models.student import Student
from tests.test_api.factories import AssessmentFactory, StudentFactory
from tests.typing import Credential

from sqlalchemy import func
from sqlalchemy.orm import scoped_session, Session, Query

from models.subject import Subject


# --- Pydantic Models for Response Validation ---
class ResponseData(BaseModel):
    """for all students data after post dump."""

    identification: str
    createdAt: str
    guardianName: str
    guardianPhone: str
    isActive: bool
    firstName_fatherName_grandFatherName: str
    grade: Optional[int]
    finalScore: Optional[float]
    rank: Optional[int]
    sectionSemesterOne: Optional[str]
    sectionSemesterTwo: Optional[str]
    averageSemesterOne: Optional[float]
    averageSemesterTwo: Optional[float]
    rankSemesterOne: Optional[int]
    rankSemesterTwo: Optional[int]


class ResponseTableId(BaseModel):
    identification: Optional[str] = None
    createdAt: Optional[str] = None
    firstName_fatherName_grandFatherName: Optional[str] = None
    guardianName: Optional[str] = None
    guardianPhone: Optional[str] = None
    isActive: Optional[str] = None
    grade: Optional[str] = None
    sectionSemesterOne: Optional[str] = None
    sectionSemesterTwo: Optional[str] = None
    averageSemesterOne: Optional[str] = None
    averageSemesterTwo: Optional[str] = None
    rankSemesterOne: Optional[str] = None
    rankSemesterTwo: Optional[str] = None
    finalScore: Optional[str] = None
    rank: Optional[str] = None


class StudentQueryResponse(BaseModel):
    tableId: ResponseTableId = ResponseTableId()
    data: List[ResponseData]


# --- Test Data Generation ---
@pytest.fixture(scope="session")
def student_data(db_session: scoped_session[Session]) -> Iterator[List[Student]]:
    """Fixture to create test student data."""
    grade_ids = db_session.query(Grade.id).order_by(Grade.grade).all()
    for grade_id in grade_ids:
        # Create 10 students for each grade
        StudentFactory.create_batch(3, grade_id=grade_id[0])

    db_session.commit()

    yield db_session.query(Student).all()


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
def stud_registerd_for_semester_one_course(
    db_session: scoped_session[Session],
    semester_one_created: Semester,
    student_data: Iterator[Student],
    all_subjects: Query[Tuple[int, int]],
) -> None:
    """Fixture to register all students in the second semester."""
    for student in student_data:
        # For each student, create assessments based on the grade
        subjects_for_registration = all_subjects.filter(
            Grade.id == student.current_grade_id
        ).all()
        for row_count, grade in subjects_for_registration:
            # Reset the sequence counter
            AssessmentFactory.reset_sequence()
            AssessmentFactory.create_batch(
                row_count, student_id=student.id, semester_id=semester_one_created.id
            )

        student.is_registered = True
        student.is_active = True
        student.semester_id = semester_one_created.id
        student.updated_at = datetime.utcnow()

    # Commit all updates to the database
    db_session.commit()


@pytest.fixture(scope="session")
def stud_registerd_for_semester_two_course(
    db_session: scoped_session[Session],
    semester_two_created: Semester,
    student_data: Iterator[Student],
    all_subjects: Query[Tuple[int, int]],
) -> None:
    """Fixture to register all students in the second semester."""
    for student in student_data:
        # For each student, create assessments based on the grade
        subjects_for_registration = all_subjects.filter(
            Grade.id == student.current_grade_id
        ).all()
        for row_count, grade in subjects_for_registration:
            # Reset the sequence counter
            AssessmentFactory.reset_sequence()
            AssessmentFactory.create_batch(
                row_count, student_id=student.id, semester_id=semester_two_created.id
            )

        student.is_registered = True

    # Commit all updates to the database
    db_session.commit()


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
