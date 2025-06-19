from typing import Any, Dict, List, Tuple
from flask.testing import FlaskClient
import pytest

from tests.test_api.fixtures.methods import is_table_sorted
from tests.typing import Credential
from tests import load_test_data


test_cases = load_test_data(
    "student_sort_advance_query.json", sort_many=True, create_sort=2
)


# --- Test Cases ---
class TestAdminStudentAdvanceSort:
    @pytest.mark.parametrize(
        "search_params",
        test_cases,
        ids=[case["sort_test_ids"] for case in test_cases],
    )
    def test_name_with_id_sorting(
        self,
        client: FlaskClient,
        register_all_students: None,
        register_stud_for_semester_one_course: None,
        register_stud_for_semester_two_course: None,
        admin_auth_header: Credential,
        search_params: Dict[str, Any],
    ) -> None:
        search_params.pop("sort_test_ids", None)

        # Build query with sorting
        response = client.post(
            "/api/v1/admin/students",
            json=search_params,
            headers=admin_auth_header["header"],
        )
        assert response.status_code == 200
        assert response.json is not None
        assert "data" in response.json

        results = response.json["data"]

        # Verify sorting
        a: List[Tuple[List[Any], bool]] = []
        skip_columns = ["createdAt"]

        for sort in search_params["sort"]:
            if sort["id"] in skip_columns:
                pytest.skip(
                    f"Skipping sort for column {sort['id']} as it is not applicable for this test."
                )

            a.append(
                (
                    [r[sort["id"]] for r in results],
                    sort["desc"],
                )
            )

        assert is_table_sorted(a)
