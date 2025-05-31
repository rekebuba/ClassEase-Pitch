from typing import Iterator, List, Dict, Any, Optional, Tuple
import factory
from flask.testing import FlaskClient
from pydantic import BaseModel, validator
from sqlalchemy import func
from sqlalchemy.orm import scoped_session, Session
import pytest

from models.grade import Grade
from models.student import Student
from models.subject import Subject
from tests.test_api.factories import AssessmentFactory, StudentFactory
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
    studentName: str
    grade: Optional[int]
    finalScore: Optional[float]
    rank: Optional[int]
    sectionI: Optional[str]
    sectionII: Optional[str]
    averageI: Optional[float]
    averageII: Optional[float]
    rankI: Optional[int]
    rankII: Optional[int]


class ResponseTableId(BaseModel):
    finalScore: str
    rank: str
    identification: str
    imagePath: str
    createdAt: str
    guardianName: str
    guardianPhone: str
    isActive: str
    studentName: List[Tuple[str, str]]
    grade: str


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
def register_all_students(
    db_session: scoped_session[Session], student_data: Iterator[Student]
) -> Iterator[Student]:
    """Fixture to register all students in the database."""
    query = (
        db_session.query(func.count().label("row_count"), Grade.grade)
        .select_from(Subject)
        .join(Grade, Subject.grade_id == Grade.id)
        .filter(Grade.grade <= 10)
        .group_by(Subject.grade_id)
        .order_by(Grade.grade)
    )
    for student in student_data:
        # For each student, create assessments based on the grade
        subjects_for_registration = query.filter(
            Grade.id == student.current_grade_id
        ).all()
        for row_count, grade in subjects_for_registration:
            # Reset the sequence counter
            AssessmentFactory.reset_sequence()
            AssessmentFactory.create_batch(row_count, student_id=student.id)

    yield db_session.query(Student).all()


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
            ([1], 3),
            ([2], 3),
            ([3], 3),
            ([4], 3),
            ([5], 3),
            ([6], 3),
            ([7], 3),
            ([8], 3),
            ([9], 3),
            ([10], 3),
            ([11], 0),
            ([12], 0),
            ([], 36),  # No grade filter should return all
        ],
    )
    def test_grade_filtering_when_all_registered(
        self,
        client: FlaskClient,
        register_all_students: List[Dict[str, Any]],
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
            ("MAS/12", 5),  # Matching pattern
            ("XYZ/99", 0),  # No matches
            ("", 50),  # Empty search returns all
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
        student_data: List[Dict[str, Any]],
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
                    "value": "MAS/12",
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

        # Verify sorting - grades should be ascending
        grades = [r["grade"] for r in results]
        assert grades == sorted(grades)

        # For students with same grade, sections should be descending
        for i in range(len(results) - 1):
            if results[i]["grade"] == results[i + 1]["grade"]:
                assert results[i]["section"] >= results[i + 1]["section"]
