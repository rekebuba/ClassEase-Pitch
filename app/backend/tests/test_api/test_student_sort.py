from flask.testing import FlaskClient
import pytest

from tests.test_api.fixtures.student_fixtures import StudentQueryResponse
from tests.typing import Credential


# --- Test Cases ---
class TestAdminStudentSorts:
    @pytest.mark.parametrize(
        "sort_by",
        [(True), (False)],
        ids=["Descending", "Ascending"],
    )
    def test_student_name_sorting(
        self,
        client: FlaskClient,
        register_all_students: None,
        register_all_students_second_semester: None,
        student_query_table_data: StudentQueryResponse,
        admin_auth_header: Credential,
        sort_by: bool,
    ) -> None:
        # Build query with sorting
        search_params = {
            "filters": [],
            "sort": [
                {
                    "id": "firstName_fatherName_grandFatherName",
                    "desc": sort_by,
                    "tableId": student_query_table_data.tableId.firstName_fatherName_grandFatherName,
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

        results = response.json["data"]
        assert len(results) > 0

        # Verify sorting
        names = [r["firstName_fatherName_grandFatherName"] for r in results]
        assert names == sorted(names, reverse=sort_by)

    @pytest.mark.parametrize(
        "sort_by",
        [(True), (False)],
        ids=["Descending", "Ascending"],
    )
    def test_student_id_sorting(
        self,
        client: FlaskClient,
        register_all_students: None,
        register_all_students_second_semester: None,
        student_query_table_data: StudentQueryResponse,
        admin_auth_header: Credential,
        sort_by: bool,
    ) -> None:
        # Build query with sorting
        search_params = {
            "filters": [],
            "sort": [
                {
                    "id": "identification",
                    "desc": sort_by,
                    "tableId": student_query_table_data.tableId.identification,
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

        results = response.json["data"]
        assert len(results) > 0

        # Verify sorting
        names = [r["identification"] for r in results]
        assert names == sorted(names, reverse=sort_by)

    @pytest.mark.parametrize(
        "sort_by",
        [(True), (False)],
        ids=["Descending", "Ascending"],
    )
    def test_student_grade_sorting(
        self,
        client: FlaskClient,
        register_all_students: None,
        register_all_students_second_semester: None,
        student_query_table_data: StudentQueryResponse,
        admin_auth_header: Credential,
        sort_by: bool,
    ) -> None:
        # Build query with sorting
        search_params = {
            "filters": [],
            "sort": [
                {
                    "id": "grade",
                    "desc": sort_by,
                    "tableId": student_query_table_data.tableId.grade,
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

        results = response.json["data"]
        assert len(results) > 0

        # Verify sorting
        names = [r["grade"] for r in results]
        assert names == sorted(names, key=lambda x: (x is not None, x), reverse=sort_by)

    @pytest.mark.parametrize(
        "sort_by",
        [(True), (False)],
        ids=["Descending", "Ascending"],
    )
    def test_section_one_sorting(
        self,
        client: FlaskClient,
        register_all_students: None,
        register_all_students_second_semester: None,
        student_query_table_data: StudentQueryResponse,
        admin_auth_header: Credential,
        sort_by: bool,
    ) -> None:
        # Build query with sorting
        search_params = {
            "filters": [],
            "sort": [
                {
                    "id": "sectionSemesterOne",
                    "desc": sort_by,
                    "tableId": student_query_table_data.tableId.sectionSemesterOne,
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

        results = response.json["data"]
        assert len(results) > 0

        # Verify sorting - sections should be in ascending order
        sections = [r["sectionSemesterOne"] for r in results]
        assert sections == sorted(
            sections, key=lambda x: (x is not None, x), reverse=sort_by
        )

    @pytest.mark.parametrize(
        "sort_by",
        [(True), (False)],
        ids=["Descending", "Ascending"],
    )
    def test_section_two_sorting(
        self,
        client: FlaskClient,
        register_all_students: None,
        register_all_students_second_semester: None,
        student_query_table_data: StudentQueryResponse,
        admin_auth_header: Credential,
        sort_by: bool,
    ) -> None:
        # Build query with sorting
        search_params = {
            "filters": [],
            "sort": [
                {
                    "id": "sectionSemesterTwo",
                    "desc": sort_by,
                    "tableId": student_query_table_data.tableId.sectionSemesterTwo,
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

        results = response.json["data"]
        assert len(results) > 0

        # Verify sorting - sections should be in ascending order
        sections = [r["sectionSemesterTwo"] for r in results]
        assert sections == sorted(
            sections, key=lambda x: (x is not None, x), reverse=sort_by
        )

    @pytest.mark.parametrize(
        "sort_by",
        [(True), (False)],
        ids=["Descending", "Ascending"],
    )
    def test_average_total_sorting(
        self,
        client: FlaskClient,
        register_all_students: None,
        register_all_students_second_semester: None,
        student_query_table_data: StudentQueryResponse,
        admin_auth_header: Credential,
        sort_by: bool,
    ) -> None:
        # Build query with sorting
        search_params = {
            "filters": [],
            "sort": [
                {
                    "id": "finalScore",
                    "desc": sort_by,
                    "tableId": student_query_table_data.tableId.finalScore,
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

        results = response.json["data"]
        assert len(results) > 0

        # Verify sorting - sections should be in ascending order
        sections = [r["finalScore"] for r in results]
        assert sections == sorted(
            sections, key=lambda x: (x is not None, x), reverse=sort_by
        )

    @pytest.mark.parametrize(
        "sort_by",
        [(True), (False)],
        ids=["Descending", "Ascending"],
    )
    def test_average_one_sorting(
        self,
        client: FlaskClient,
        register_all_students: None,
        register_all_students_second_semester: None,
        student_query_table_data: StudentQueryResponse,
        admin_auth_header: Credential,
        sort_by: bool,
    ) -> None:
        # Build query with sorting
        search_params = {
            "filters": [],
            "sort": [
                {
                    "id": "averageSemesterOne",
                    "desc": sort_by,
                    "tableId": student_query_table_data.tableId.averageSemesterOne,
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

        results = response.json["data"]
        assert len(results) > 0

        # Verify sorting - sections should be in ascending order
        sections = [r["averageSemesterOne"] for r in results]
        assert sections == sorted(
            sections, key=lambda x: (x is not None, x), reverse=sort_by
        )

    @pytest.mark.parametrize(
        "sort_by",
        [(True), (False)],
        ids=["Descending", "Ascending"],
    )
    def test_average_two_sorting(
        self,
        client: FlaskClient,
        register_all_students: None,
        register_all_students_second_semester: None,
        student_query_table_data: StudentQueryResponse,
        admin_auth_header: Credential,
        sort_by: bool,
    ) -> None:
        # Build query with sorting
        search_params = {
            "filters": [],
            "sort": [
                {
                    "id": "averageSemesterTwo",
                    "desc": sort_by,
                    "tableId": student_query_table_data.tableId.averageSemesterTwo,
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

        results = response.json["data"]
        assert len(results) > 0

        # Verify sorting - sections should be in ascending order
        sections = [r["averageSemesterTwo"] for r in results]
        assert sections == sorted(
            sections, key=lambda x: (x is not None, x), reverse=sort_by
        )

    @pytest.mark.parametrize(
        "sort_by",
        [(True), (False)],
        ids=["Descending", "Ascending"],
    )
    def test_rank_total_sorting(
        self,
        client: FlaskClient,
        register_all_students: None,
        register_all_students_second_semester: None,
        student_query_table_data: StudentQueryResponse,
        admin_auth_header: Credential,
        sort_by: bool,
    ) -> None:
        # Build query with sorting
        search_params = {
            "filters": [],
            "sort": [
                {
                    "id": "rank",
                    "desc": sort_by,
                    "tableId": student_query_table_data.tableId.rank,
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

        results = response.json["data"]
        assert len(results) > 0

        # Verify sorting - sections should be in ascending order
        sections = [r["rank"] for r in results]
        assert sections == sorted(
            sections, key=lambda x: (x is not None, x), reverse=sort_by
        )

    @pytest.mark.parametrize(
        "sort_by",
        [(True), (False)],
        ids=["Descending", "Ascending"],
    )
    def test_rank_one_sorting(
        self,
        client: FlaskClient,
        register_all_students: None,
        register_all_students_second_semester: None,
        student_query_table_data: StudentQueryResponse,
        admin_auth_header: Credential,
        sort_by: bool,
    ) -> None:
        # Build query with sorting
        search_params = {
            "filters": [],
            "sort": [
                {
                    "id": "rankSemesterOne",
                    "desc": sort_by,
                    "tableId": student_query_table_data.tableId.rankSemesterOne,
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

        results = response.json["data"]
        assert len(results) > 0

        # Verify sorting - sections should be in ascending order
        sections = [r["rankSemesterOne"] for r in results]
        assert sections == sorted(
            sections, key=lambda x: (x is not None, x), reverse=sort_by
        )

    @pytest.mark.parametrize(
        "sort_by",
        [(True), (False)],
        ids=["Descending", "Ascending"],
    )
    def test_rank_two_sorting(
        self,
        client: FlaskClient,
        register_all_students: None,
        register_all_students_second_semester: None,
        student_query_table_data: StudentQueryResponse,
        admin_auth_header: Credential,
        sort_by: bool,
    ) -> None:
        # Build query with sorting
        search_params = {
            "filters": [],
            "sort": [
                {
                    "id": "rankSemesterTwo",
                    "desc": sort_by,
                    "tableId": student_query_table_data.tableId.rankSemesterTwo,
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

        results = response.json["data"]
        assert len(results) > 0

        # Verify sorting - sections should be in ascending order
        sections = [r["rankSemesterTwo"] for r in results]
        assert sections == sorted(
            sections, key=lambda x: (x is not None, x), reverse=sort_by
        )

    @pytest.mark.parametrize(
        "sort_by",
        [(True), (False)],
        ids=["Descending", "Ascending"],
    )
    def test_gurdian_name_sorting(
        self,
        client: FlaskClient,
        register_all_students: None,
        register_all_students_second_semester: None,
        student_query_table_data: StudentQueryResponse,
        admin_auth_header: Credential,
        sort_by: bool,
    ) -> None:
        # Build query with sorting
        search_params = {
            "filters": [],
            "sort": [
                {
                    "id": "guardianName",
                    "desc": sort_by,
                    "tableId": student_query_table_data.tableId.guardianName,
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

        results = response.json["data"]
        assert len(results) > 0

        # Verify sorting
        names = [r["guardianName"] for r in results]
        assert names == sorted(names, reverse=sort_by)

    @pytest.mark.parametrize(
        "sort_by",
        [(True), (False)],
        ids=["Descending", "Ascending"],
    )
    def test_gurdian_phone_sorting(
        self,
        client: FlaskClient,
        register_all_students: None,
        register_all_students_second_semester: None,
        student_query_table_data: StudentQueryResponse,
        admin_auth_header: Credential,
        sort_by: bool,
    ) -> None:
        # Build query with sorting
        search_params = {
            "filters": [],
            "sort": [
                {
                    "id": "guardianPhone",
                    "desc": sort_by,
                    "tableId": student_query_table_data.tableId.guardianPhone,
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

        results = response.json["data"]
        assert len(results) > 0

        # Verify sorting
        names = [r["guardianPhone"] for r in results]
        assert names == sorted(names, reverse=sort_by)

    @pytest.mark.parametrize(
        "sort_by",
        [(True), (False)],
        ids=["Descending", "Ascending"],
    )
    def test_joind_date_sorting(
        self,
        client: FlaskClient,
        register_all_students: None,
        register_all_students_second_semester: None,
        student_query_table_data: StudentQueryResponse,
        admin_auth_header: Credential,
        sort_by: bool,
    ) -> None:
        # Build query with sorting
        search_params = {
            "filters": [],
            "sort": [
                {
                    "id": "createdAt",
                    "desc": sort_by,
                    "tableId": student_query_table_data.tableId.createdAt,
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

        results = response.json["data"]
        assert len(results) > 0

        # Verify sorting
        names = [r["createdAt"] for r in results]
        assert names == sorted(names, reverse=sort_by)
