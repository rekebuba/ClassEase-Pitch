import random
from typing import List
import pytest
from flask.testing import FlaskClient
from extension.pydantic.models.subject_schema import SubjectSchema
from models.year import Year
from tests.test_api.dynamic_schema import DynamicSchema
from tests.typing import Credential

from tests.test_api._helpers import _validate_invalid_fields_response


class TestSubjectsApi:
    @pytest.mark.parametrize(
        "test_case, fields, expected_status",
        [
            ("no_fields", None, 200),
            (
                "valid_fields",
                random.sample(
                    list(SubjectSchema.model_fields.keys()),
                    k=random.randint(1, len(SubjectSchema.model_fields.keys())),
                ),
                200,
            ),
            (
                "invalid_fields",
                list(
                    set(
                        random.sample(
                            list(SubjectSchema.model_fields.keys()),
                            k=random.randint(1, len(SubjectSchema.model_fields.keys())),
                        )
                        + ["invalid1", "invalid2"]
                    )
                ),
                400,
            ),
        ],
        ids=["no-fields", "valid-fields", "invalid-fields"],
    )
    def test_get_subjects(
        self,
        academic_year: Year,
        client: FlaskClient,
        random_auth_header: Credential,
        test_case: str,
        fields: list[str] | None,
        expected_status: int,
    ) -> None:
        """Test the API endpoint for retrieving all subjects with various field selections."""
        url = f"/api/v1/years/{academic_year.id}/subjects"
        if fields:
            url += f"?fields={','.join(fields)}"

        response = client.get(url, headers=random_auth_header["header"])

        assert response.status_code == expected_status
        assert response.json is not None

        if expected_status == 200:
            expected_fields = (
                fields if fields is not None else SubjectSchema.default_fields()
            )
            DynamicSchema.validate_response(
                response_data=response.json,
                base_model=SubjectSchema,
                expected_fields=expected_fields,
                type="list",
            )
        elif expected_status == 400:
            allowed_fields = set(SubjectSchema.model_fields.keys())
            invalid_fields = set(fields if fields else []) - allowed_fields
            _validate_invalid_fields_response(response.json, invalid_fields)

    @pytest.mark.parametrize(
        "test_case, fields, expected_status",
        [
            ("no_fields", None, 200),
            (
                "valid_fields",
                random.sample(
                    list(SubjectSchema.model_fields.keys()),
                    k=random.randint(1, len(SubjectSchema.model_fields.keys())),
                ),
                200,
            ),
            (
                "invalid_fields",
                list(
                    set(
                        random.sample(
                            list(SubjectSchema.model_fields.keys()),
                            k=random.randint(1, len(SubjectSchema.model_fields.keys())),
                        )
                        + ["invalid1", "invalid2"]
                    )
                ),
                400,
            ),
        ],
        ids=["no-fields", "valid-fields", "invalid-fields"],
    )
    def test_get_subject_by_id(
        self,
        academic_year: Year,
        client: FlaskClient,
        subjects: List[SubjectSchema],
        random_auth_header: Credential,
        test_case: str,
        fields: list[str] | None,
        expected_status: int,
    ) -> None:
        """Test the API endpoint for retrieving a single subject by ID with various field selections."""
        subject_id = random.choice(subjects).id
        url = f"/api/v1/years/{academic_year.id}/subjects/{subject_id}"
        if fields:
            url += f"?fields={','.join(fields)}"

        response = client.get(url, headers=random_auth_header["header"])

        assert response.status_code == expected_status
        assert response.json is not None

        if expected_status == 200:
            expected_fields = (
                fields if fields is not None else SubjectSchema.default_fields()
            )
            DynamicSchema.validate_response(
                response_data=response.json,
                base_model=SubjectSchema,
                expected_fields=expected_fields,
            )
        elif expected_status == 400:
            allowed_fields = set(SubjectSchema.model_fields.keys())
            invalid_fields = set(fields if fields else []) - allowed_fields
            _validate_invalid_fields_response(response.json, invalid_fields)

    def test_get_subjects_unauthorized(
        self,
        client: FlaskClient,
        academic_year: Year,
    ) -> None:
        """Test that a 401 error is returned when no auth header is provided."""
        url = f"/api/v1/years/{academic_year.id}/subjects"
        response = client.get(url)

        assert response.status_code == 401

    def test_get_subject_by_id_unauthorized(
        self,
        client: FlaskClient,
        academic_year: Year,
        subjects: List[SubjectSchema],
    ) -> None:
        """Test that a 401 error is returned when no auth header is provided."""
        subject_id = random.choice(subjects).id
        url = f"/api/v1/years/{academic_year.id}/subjects/{subject_id}"
        response = client.get(url)

        assert response.status_code == 401

    def test_get_subject_by_id_not_found(
        self,
        client: FlaskClient,
        random_auth_header: Credential,
        academic_year: Year,
    ) -> None:
        """Test that a 404 error is returned for a non-existent subject ID."""
        non_existent_subject_id = 99999  # An ID that is unlikely to exist
        url = f"/api/v1/years/{academic_year.id}/subjects/{non_existent_subject_id}"
        response = client.get(url, headers=random_auth_header["header"])

        assert response.status_code == 404
