from typing import Callable, List, Dict, Any, Set, Union
from flask.testing import FlaskClient
import pytest
from pyethiodate import EthDate  # type: ignore
from datetime import datetime

from tests import json_test_data
from tests.test_api.fixtures.student_fixtures import StudentQueryResponse
from tests.typing import Credential, RangeDict


current_year = int(EthDate.date_to_ethiopian(datetime.now()).year)

templates = json_test_data["filter_templates"]
filters = json_test_data["simple_filter"]

test_ids = []
test_param = []

# Prepare test cases
for filter in filters:
    options = filter["options"]
    for option in options:
        for operator in filter["operators"]:
            test_ids.append(f"{filter['id']}_{operator}_{option.get('id')}")
            test_param.append((templates[filter["template"]], option, operator))


# --- Test Cases ---
class TestAdminStudentQueries:
    @pytest.mark.parametrize("filter, value, operator", test_param, ids=test_ids)
    def test_filtering_when_all_registered(
        self,
        client: FlaskClient,
        student_data: List[Dict[str, Any]],
        register_stud_for_semester_one_course: None,
        register_stud_for_semester_two_course: None,
        admin_auth_header: Credential,
        student_query_table_data: StudentQueryResponse,
        filter: Dict[str, Any],
        value: Dict[str, Any],
        operator: str,
        admin_student_avrage_range: Dict[str, Any],
    ) -> None:
        # Build query
        column_id = filter["id"]
        table_id = student_query_table_data.tableId

        filter["tableId"] = getattr(table_id, column_id)
        filter["value"] = value["value"]
        filter["operator"] = operator

        search_params = {
            "filters": [filter],
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

        # check only the expected valus exists
        result: Set[Any] = {r[column_id] for r in response.json["data"]}
        OPERATORS: Dict[
            str, Callable[[Set[Any], Union[List[Any], RangeDict]], bool]
        ] = {
            "in": lambda x, y: x == set(y),
            "notIn": lambda x, y: not x > set(y),
            "isBetween": lambda x, y: all(
                (y["min"] <= item <= y["max"])
                if isinstance(y, dict) and "min" in y and "max" in y
                else False
                for item in x
            ),
            "isNotBetween": lambda x, y: all(
                (item < y["min"] and item > y["max"])
                if isinstance(y, dict) and "min" in y and "max" in y
                else False
                for item in x
            ),
        }
        assert OPERATORS[operator](result, value["value"]), (
            f"Failed for {filter['id']} with operator {operator}"
        )

    def test_complex_query_with_sorting(
        self,
        client: FlaskClient,
        register_all_students: List[Dict[str, Any]],
        register_stud_for_semester_one_course: None,
        register_stud_for_semester_two_course: None,
        student_query_table_data: StudentQueryResponse,
        admin_auth_header: Credential,
    ) -> None:
        search_params = {
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
                    "value": "MAS/",
                },
                {
                    "tableId": student_query_table_data.tableId.sectionSemesterOne,
                    "id": "sectionSemesterOne",
                    "variant": "multiSelect",
                    "operator": "in",
                    "value": ["A", "B"],
                },
            ],
            "sort": [
                {
                    "id": "grade",
                    "desc": False,
                    "tableId": student_query_table_data.tableId.grade,
                },
                {
                    "tableId": student_query_table_data.tableId.sectionSemesterOne,
                    "id": "sectionSemesterOne",
                    "desc": True,
                },
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
                assert (
                    results[i]["sectionSemesterOne"]
                    >= results[i + 1]["sectionSemesterOne"]
                )
