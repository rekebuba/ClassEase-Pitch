from itertools import groupby
from operator import itemgetter
from typing import Any, Dict
from flask.testing import FlaskClient
import pytest

from tests.test_api.fixtures.student_fixtures import StudentQueryResponse
from tests.typing import Credential
from tests import json_test_data

# Read and prepare data at module level
raw_data = json_test_data["advance_sort"]

# Create a list of tuples for parametrize
test_param = [tuple(case["sort"]) for case in raw_data]
test_ids = [case["id"] for case in raw_data]


# --- Test Cases ---
class TestAdminStudentAdvanceSort:
    @pytest.mark.parametrize("sort", test_param, ids=test_ids)
    def test_name_with_id_sorting(
        self,
        client: FlaskClient,
        register_all_students: None,
        stud_registerd_for_semester_two_course: None,
        student_query_table_data: StudentQueryResponse,
        admin_auth_header: Credential,
        sort: tuple[Dict[str, Any], Dict[str, Any]],
    ) -> None:
        # Build query with sorting
        first_id = sort[0]["id"]
        sort_first = sort[0]["desc"]

        second_id = sort[1]["id"]
        sort_second = sort[1]["desc"]

        table_ids = student_query_table_data.tableId

        sort[0]["tableId"] = getattr(table_ids, first_id)
        sort[1]["tableId"] = getattr(table_ids, second_id)

        search_params = {
            "sort": [sort[0], sort[1]],
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
        assert len(results) == 10  # same as per_page

        # Verify sorting
        names = [r[first_id] for r in results]
        assert names == sorted(
            names, key=lambda x: (x is not None, x), reverse=sort_first
        )

        # Group by identification (primary key)
        grouped = groupby(
            sorted(results, key=lambda r: (r[first_id] is not None, r[first_id])),
            key=itemgetter(first_id),
        )

        # Within each group, check if the second column is sorted (with null-safe sort)
        for _, group in grouped:
            group_list = list(group)
            second_column = [r[second_id] for r in group_list]
            assert second_column == sorted(
                second_column,
                key=lambda x: (x is not None, x),
                reverse=sort_second,
            ), f"Secondary sort failed for group: {group_list}"
