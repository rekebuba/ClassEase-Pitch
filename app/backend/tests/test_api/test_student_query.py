from typing import Iterator, List, Dict, Any, Optional, Tuple
import factory
from flask.testing import FlaskClient
from pydantic import BaseModel, validator
from sqlalchemy import func
from sqlalchemy.orm import scoped_session, Session, Query
import pytest
from pyethiodate import EthDate  # type: ignore
from datetime import datetime

from models.grade import Grade
from models.student import Student
from models.subject import Subject
from tests.test_api.factories import AssessmentFactory, SemesterFactory, StudentFactory
from tests.typing import Credential


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
    sectionSemesterOne: Optional[str]
    sectionSemesterTwo: Optional[str]
    averageSemesterOne: Optional[float]
    averageSemesterTwo: Optional[float]
    rankSemesterOne: Optional[int]
    rankSemesterTwo: Optional[int]


class ResponseTableId(BaseModel):
    finalScore: str
    rank: str
    identification: str
    imagePath: str
    createdAt: str
    guardianName: str
    guardianPhone: str
    isActive: str
    firstName_fatherName_grandFatherName: str
    grade: str


class StudentQueryResponse(BaseModel):
    tableId: ResponseTableId
    data: List[ResponseData]


current_year = int(EthDate.date_to_ethiopian(datetime.now()).year)


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


# --- Test Cases ---
class TestAdminStudentQueries:
    @pytest.mark.parametrize(
        "grades,expected_count",
        [
            ([1, 2, 3], 0),
            ([10, 11], 0),
            ([5, 6, 7, 8], 0),
            ([1, 3, 9, 2, 4], 0),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 0),
            ([], 36),  # No grade filter should return all
        ],
    )
    def test_grade_filtering_when_no_one_registered(
        self,
        client: FlaskClient,
        student_data: List[Dict[str, Any]],
        admin_auth_header: Credential,
        grades: List[int],
        expected_count: int,
    ) -> None:
        # Get table IDs first
        table_resp = client.post(
            "/api/v1/admin/students", json={}, headers=admin_auth_header["header"]
        )
        assert table_resp.status_code == 200
        assert table_resp.json is not None

        table_data = StudentQueryResponse(**table_resp.json)

        # Build query
        search_params = {
            "filters": [
                {
                    "tableId": table_data.tableId.grade,
                    "id": "grade",
                    "variant": "multiSelect",
                    "operator": "in",
                    "value": grades,
                }
            ],
            "page": 1,
            "perPage": 50,
        }

        response = client.post(
            "/api/v1/admin/students",
            json=search_params,
            headers=admin_auth_header["header"],
        )
        assert response.status_code == 200
        assert response.json is not None
        assert "data" in response.json
        assert isinstance(response.json["data"], list)
        assert len(response.json["data"]) == expected_count

    @pytest.mark.parametrize(
        "grades,expected_count",
        [
            ([11], 0),  # No student registered for corse in grade 11
            ([12], 0),  # No student registered for corse in grade 12
            ([11, 12], 0),
            ([1], 3),
            ([3], 3),
            ([8], 3),
            ([9, 10], 6),
            ([10, 11], 3),
            ([10, 11, 12], 3),
            ([10, 9, 12], 6),
            ([1, 2, 3], 9),
            ([5, 6, 7, 8], 12),
            ([1, 3, 9, 2, 4], 15),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 30),
            ([], 36),  # No grade filter should return all
        ],
    )
    def test_grade_filtering_when_all_registered(
        self,
        client: FlaskClient,
        register_all_students: None,
        register_all_students_second_semester: None,
        admin_auth_header: Credential,
        grades: List[int],
        expected_count: int,
    ) -> None:
        # Get table IDs first
        table_resp = client.post(
            "/api/v1/admin/students", json={}, headers=admin_auth_header["header"]
        )
        assert table_resp.status_code == 200
        assert table_resp.json is not None

        table_data = StudentQueryResponse(**table_resp.json)

        # Build query
        search_params = {
            "filters": [
                {
                    "tableId": table_data.tableId.grade,
                    "id": "grade",
                    "variant": "multiSelect",
                    "operator": "in",
                    "value": grades,
                }
            ],
            "page": 1,
            "perPage": 50,
        }

        response = client.post(
            "/api/v1/admin/students",
            json=search_params,
            headers=admin_auth_header["header"],
        )
        assert response.status_code == 200
        assert response.json is not None
        assert "data" in response.json
        assert isinstance(response.json["data"], list)
        assert len(response.json["data"]) == expected_count

    @pytest.mark.parametrize(
        "search_term,expected_matches",
        [
            (f"MAS/1015/{current_year % 100}", 1),
            ("MAS/1011/", 1),
            ("MAS/1011/11", 0),
            ("XYZ/1011/12", 0),
            ("aldsflkdf", 0),
            ("MAA/", 0),
            ("MAT/", 0),
            ("MAS/101", 10),  # Multiple matches
            ("", 36),  # Empty search returns all
        ],
    )
    def test_identification_search(
        self,
        client: FlaskClient,
        student_data: List[Dict[str, Any]],
        admin_auth_header: Credential,
        search_term: str,
        expected_matches: int,
    ) -> None:
        table_resp = client.post(
            "/api/v1/admin/students", json={}, headers=admin_auth_header["header"]
        )
        assert table_resp.status_code == 200
        assert table_resp.json is not None

        table_data = StudentQueryResponse(**table_resp.json)

        search_params = {
            "filters": [
                {
                    "tableId": table_data.tableId.identification,
                    "id": "identification",
                    "variant": "text",
                    "operator": "iLike",
                    "value": search_term,
                }
            ],
            "page": 1,
            "per_page": 50,
        }

        response = client.post(
            "/api/v1/admin/students",
            json=search_params,
            headers=admin_auth_header["header"],
        )
        assert response.status_code == 200
        assert response.json is not None
        assert "data" in response.json
        assert len(response.json["data"]) == expected_matches

    def test_complex_query_with_sorting(
        self,
        client: FlaskClient,
        register_all_students: List[Dict[str, Any]],
        admin_auth_header: Credential,
    ) -> None:
        table_resp = client.post(
            "/api/v1/admin/students", json={}, headers=admin_auth_header["header"]
        )
        assert table_resp.status_code == 200
        assert table_resp.json is not None

        table_data = StudentQueryResponse(**table_resp.json)

        search_params = {
            "join_operator": "or",
            "filters": [
                {
                    "tableId": table_data.tableId.grade,
                    "id": "grade",
                    "variant": "multiSelect",
                    "operator": "in",
                    "value": [1, 2, 3],
                },
                {
                    "tableId": table_data.tableId.identification,
                    "id": "identification",
                    "variant": "text",
                    "operator": "iLike",
                    "value": "MAS/101",
                },
                {
                    "id": "section",
                    "variant": "multiSelect",
                    "operator": "in",
                    "value": ["A", "B"],
                },
            ],
            "sorts": [
                {
                    "id": "grade",
                    "desc": False,
                    "tableId": table_data.tableId.grade,
                },
                {"id": "section", "desc": True},
            ],
            "page": 1,
            "per_page": 10,
        }

        response = client.post(
            "/api/v1/admin/students",
            json=search_params,
            headers=admin_auth_header["header"],
        )
        assert response.status_code == 200
        assert response.json is not None
        assert "data" in response.json

        results = response.json["data"]

        assert len(results) == 10  # same as per_page

        # Verify sorting - grades should be ascending
        grades = [r["grade"] for r in results]
        assert grades == sorted(grades)

        # For students with same grade, sections should be descending
        for i in range(len(results) - 1):
            if results[i]["grade"] == results[i + 1]["grade"]:
                assert results[i]["section"] >= results[i + 1]["section"]
