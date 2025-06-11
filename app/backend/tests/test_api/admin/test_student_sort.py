from typing import Any, Dict
from flask.testing import FlaskClient
import pytest

from tests import json_test_data
from tests.test_api.fixtures.student_fixtures import StudentQueryResponse
from tests.typing import Credential

# Read and prepare data at module level
raw_data = json_test_data["simple_sort"]

# Create a list of tuples for parametrize
test_param = [tuple(case["sort"]) for case in raw_data]
test_ids = [case["id"] for case in raw_data]


# --- Test Cases ---
class TestAdminStudentSorts:
    @pytest.mark.parametrize("sort", test_param, ids=test_ids)
    def test_student_name_sorting(
        self,
        client: FlaskClient,
        register_all_students: None,
        stud_registerd_for_semester_one_course: None,
        stud_registerd_for_semester_two_course: None,
        student_query_table_data: StudentQueryResponse,
        admin_auth_header: Credential,
        sort: tuple[Dict[str, Any], Dict[str, Any]],
    ) -> None:
        first_id = sort[0]["id"]
        sort_first = sort[0]["desc"]

        table_ids = student_query_table_data.tableId

        sort[0]["tableId"] = getattr(table_ids, first_id)
        # Build query with sorting
        search_params = {
            "sort": [sort[0]],
            "filters": [],
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
        assert len(results) > 0

        # Verify sorting
        names = [r[first_id] for r in results]
        assert names == sorted(
            names, key=lambda x: (x is not None, x), reverse=sort_first
        )
