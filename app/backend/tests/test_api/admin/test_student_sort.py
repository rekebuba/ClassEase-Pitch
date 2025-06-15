from typing import Any, Dict
from flask.testing import FlaskClient
import pytest

from tests import load_test_data
from tests.typing import Credential


test_cases = load_test_data("student_sort_query.json", sort_many=False)


# --- Test Cases ---
class TestAdminStudentSorts:
    @pytest.mark.parametrize(
        "search_params",
        test_cases,
        ids=[case["sort_test_ids"] for case in test_cases],
    )
    def test_student_name_sorting(
        self,
        client: FlaskClient,
        register_all_students: None,
        register_stud_for_semester_one_course: None,
        register_stud_for_semester_two_course: None,
        admin_auth_header: Credential,
        search_params: Dict[str, Any],
    ) -> None:
        search_params.pop("sort_test_ids", None)

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
        first_id = search_params["sort"][0].get("id")
        sort_first = search_params["sort"][0].get("desc", False)
        assert first_id is not None, "Sort ID must be provided in search params"

        names = [r[first_id] for r in results]
        assert names == sorted(
            names, key=lambda x: (x is not None, x), reverse=sort_first
        )
