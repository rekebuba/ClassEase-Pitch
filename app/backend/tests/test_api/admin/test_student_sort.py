from dataclasses import asdict
from typing import Any, Dict
from flask.testing import FlaskClient

from tests.test_api.factories import QueryFactory, TableIdFactory
from tests.typing import Credential


def pytest_generate_tests(metafunc):
    if "search_params" in metafunc.fixturenames:
        table_id = TableIdFactory.create()
        search_params = QueryFactory.create_batch(
            tableId=asdict(table_id), get_sort=True, size=20
        )

        # test_ids = [
        #     f"{case.sort[0].id}-{'desc' if case.sort[0].desc else 'asc'}"
        #     for case in search_params
        # ]

        metafunc.parametrize(
            "search_params",
            [asdict(param) for param in search_params],
        )


# --- Test Cases ---
class TestAdminStudentSorts:
    def test_student_name_sorting(
        self,
        client: FlaskClient,
        register_all_students: None,
        stud_registerd_for_semester_one_course: None,
        stud_registerd_for_semester_two_course: None,
        admin_auth_header: Credential,
        search_params: Dict[str, Any],
    ) -> None:
        search_params.pop("columns")
        search_params.pop("table_name")

        # test_id = f"{search_params['sort'][0]['id']}-{'desc' if search_params['sort'][0]['desc'] else 'asc'}"

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
