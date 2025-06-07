from itertools import groupby
from operator import itemgetter
from flask.testing import FlaskClient
import pytest

from tests.test_api.fixtures.student_fixtures import StudentQueryResponse
from tests.typing import Credential


# --- Test Cases ---
class TestAdminStudentAdvanceSort:
    @pytest.mark.parametrize(
        "sort_by, ",
        [(True), (False)],
        ids=["Descending", "Ascending"],
    )
    def test_name_with_id_sorting(
        self,
        client: FlaskClient,
        # register_all_students: None,
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
                },
                {
                    "id": "grade",
                    "desc": sort_by,
                    "tableId": student_query_table_data.tableId.grade,
                },
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

        # for the same first sort, # verify the second sort
        # Group by identification
        grouped = groupby(
            sorted(results, key=itemgetter("identification")),
            key=itemgetter("identification"),
        )

        # Within each group, check if second column is sorted
        for _, group in grouped:
            group_list = list(group)
            second_column = [r["grade"] for r in group_list]
            assert second_column == sorted(second_column), (
                f"Secondary sort failed for group: {group_list}"
            )
