from typing import List, Dict, Any
from flask.testing import FlaskClient
import pytest
from pyethiodate import EthDate  # type: ignore
from datetime import datetime

from tests.test_api.fixtures.student_fixtures import StudentQueryResponse
from tests.typing import Credential


current_year = int(EthDate.date_to_ethiopian(datetime.now()).year)


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
        student_query_table_data: StudentQueryResponse,
        grades: List[int],
        expected_count: int,
    ) -> None:
        # Build query
        search_params = {
            "filters": [
                {
                    "tableId": student_query_table_data.tableId.grade,
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
        student_query_table_data: StudentQueryResponse,
        grades: List[int],
        expected_count: int,
    ) -> None:
        # Build query
        search_params = {
            "filters": [
                {
                    "tableId": student_query_table_data.tableId.grade,
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
        "sections_semester_one,expected_count",
        [
            (["A", "B", "C"], 30),  # All students who registered in semester one
            (["A", "B", "C", "F", "G"], 30),
        ],
    )
    def test_section_one_filtering(
        self,
        client: FlaskClient,
        register_all_students: None,
        admin_auth_header: Credential,
        student_query_table_data: StudentQueryResponse,
        sections_semester_one: List[str],
        expected_count: int,
    ) -> None:
        # Build query
        search_params = {
            "filters": [
                {
                    "tableId": student_query_table_data.tableId.sectionSemesterOne,
                    "id": "sectionSemesterOne",
                    "variant": "multiSelect",
                    "operator": "in",
                    "value": sections_semester_one,
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
        "sections_semester_two,expected_count",
        [
            (["A", "B", "C"], 30),  # All students who registered in semester one
            (["A", "B", "C", "F", "G"], 30),
        ],
    )
    def test_section_two_filtering(
        self,
        client: FlaskClient,
        register_all_students: None,
        register_all_students_second_semester: None,
        admin_auth_header: Credential,
        student_query_table_data: StudentQueryResponse,
        sections_semester_two: List[str],
        expected_count: int,
    ) -> None:
        # Build query
        search_params = {
            "filters": [
                {
                    "tableId": student_query_table_data.tableId.sectionSemesterTwo,
                    "id": "sectionSemesterTwo",
                    "variant": "multiSelect",
                    "operator": "in",
                    "value": sections_semester_two,
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
        register_all_students_second_semester: None,
        admin_auth_header: Credential,
        student_query_table_data: StudentQueryResponse,
        search_term: str,
        expected_matches: int,
    ) -> None:
        search_params = {
            "filters": [
                {
                    "tableId": student_query_table_data.tableId.identification,
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
        student_query_table_data: StudentQueryResponse,
        admin_auth_header: Credential,
    ) -> None:
        search_params = {
            "join_operator": "or",
            "filters": [
                {
                    "tableId": student_query_table_data.tableId.grade,
                    "id": "grade",
                    "variant": "multiSelect",
                    "operator": "in",
                    "value": [1, 2, 3],
                },
                {
                    "tableId": student_query_table_data.tableId.identification,
                    "id": "identification",
                    "variant": "text",
                    "operator": "iLike",
                    "value": "MAS/101",
                },
                {
                    "tableId": student_query_table_data.tableId.sectionSemesterOne,
                    "id": "sectionSemesterOne",
                    "variant": "multiSelect",
                    "operator": "in",
                    "value": ["A", "B"],
                },
            ],
            "sorts": [
                {
                    "id": "grade",
                    "desc": False,
                    "tableId": student_query_table_data.tableId.grade,
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
