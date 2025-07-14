import random
from typing import List
import pytest
from flask.testing import FlaskClient
from extension.pydantic.models.grade_schema import GradeSchema
from models.year import Year
from tests.test_api.dynamic_schema import DynamicSchema
from tests.typing import Credential

from tests.test_api._helpers import _validate_invalid_fields_response


class TestGradesApi:
    @pytest.mark.parametrize(
        "test_case, fields, expected_status",
        [
            ("no_fields", None, 200),
            (
                "valid_fields",
                random.sample(
                    list(GradeSchema.model_fields.keys()),
                    k=random.randint(1, len(GradeSchema.model_fields.keys())),
                ),
                200,
            ),
            (
                "invalid_fields",
                list(
                    set(
                        random.sample(
                            list(GradeSchema.model_fields.keys()),
                            k=random.randint(1, len(GradeSchema.model_fields.keys())),
                        )
                        + ["invalid1", "invalid2"]
                    )
                ),
                400,
            ),
        ],
        ids=["no-fields", "valid-fields", "invalid-fields"],
    )
    def test_get_grades(
        self,
        academic_year: Year,
        client: FlaskClient,
        random_auth_header: Credential,
        test_case: str,
        fields: list[str] | None,
        expected_status: int,
    ) -> None:
        """Test the API endpoint for retrieving all grades with various field selections."""
        url = f"/api/v1/years/{academic_year.id}/grades"
        if fields:
            url += f"?fields={','.join(fields)}"

        response = client.get(url, headers=random_auth_header["header"])

        assert response.status_code == expected_status
        assert response.json is not None

        if expected_status == 200:
            expected_fields = (
                fields if fields is not None else GradeSchema.default_fields()
            )
            DynamicSchema.validate_response(
                response_data=response.json,
                base_model=GradeSchema,
                expected_fields=expected_fields,
                type="list",
            )
        elif expected_status == 400:
            allowed_fields = set(GradeSchema.model_fields.keys())
            invalid_fields = set(fields if fields else []) - allowed_fields
            _validate_invalid_fields_response(response.json, invalid_fields)

    @pytest.mark.parametrize(
        "test_case, fields, expected_status",
        [
            ("no_fields", None, 200),
            (
                "valid_fields",
                random.sample(
                    list(GradeSchema.model_fields.keys()),
                    k=random.randint(1, len(GradeSchema.model_fields.keys())),
                ),
                200,
            ),
            (
                "invalid_fields",
                list(
                    set(
                        random.sample(
                            list(GradeSchema.model_fields.keys()),
                            k=random.randint(1, len(GradeSchema.model_fields.keys())),
                        )
                        + ["invalid1", "invalid2"]
                    )
                ),
                400,
            ),
        ],
        ids=["no-fields", "valid-fields", "invalid-fields"],
    )
    def test_get_grade_by_id(
        self,
        academic_year: Year,
        client: FlaskClient,
        grades: List[GradeSchema],
        random_auth_header: Credential,
        test_case: str,
        fields: list[str] | None,
        expected_status: int,
    ) -> None:
        """Test the API endpoint for retrieving a single grade by ID with various field selections."""
        grade_id = random.choice(grades).id
        url = f"/api/v1/years/{academic_year.id}/grades/{grade_id}"
        if fields:
            url += f"?fields={','.join(fields)}"

        response = client.get(url, headers=random_auth_header["header"])

        assert response.status_code == expected_status
        assert response.json is not None

        if expected_status == 200:
            expected_fields = (
                fields if fields is not None else GradeSchema.default_fields()
            )
            DynamicSchema.validate_response(
                response_data=response.json,
                base_model=GradeSchema,
                expected_fields=expected_fields,
            )
        elif expected_status == 400:
            allowed_fields = set(GradeSchema.model_fields.keys())
            invalid_fields = set(fields if fields else []) - allowed_fields
            _validate_invalid_fields_response(response.json, invalid_fields)

    def test_get_grades_unauthorized(
        self,
        client: FlaskClient,
        academic_year: Year,
    ) -> None:
        """Test that a 401 error is returned when no auth header is provided."""
        url = f"/api/v1/years/{academic_year.id}/grades"
        response = client.get(url)

        assert response.status_code == 401

    def test_get_grade_by_id_unauthorized(
        self,
        client: FlaskClient,
        academic_year: Year,
        grades: List[GradeSchema],
    ) -> None:
        """Test that a 401 error is returned when no auth header is provided."""
        grade_id = random.choice(grades).id
        url = f"/api/v1/years/{academic_year.id}/grades/{grade_id}"
        response = client.get(url)

        assert response.status_code == 401

    def test_get_grade_by_id_not_found(
        self,
        client: FlaskClient,
        random_auth_header: Credential,
        academic_year: Year,
    ) -> None:
        """Test that a 404 error is returned for a non-existent grade ID."""
        non_existent_grade_id = 99999  # An ID that is unlikely to exist
        url = f"/api/v1/years/{academic_year.id}/grades/{non_existent_grade_id}"
        response = client.get(url, headers=random_auth_header["header"])

        assert response.status_code == 404
