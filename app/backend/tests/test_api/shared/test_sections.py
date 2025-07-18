import random
from typing import List
import pytest
from flask.testing import FlaskClient
from extension.pydantic.models.section_schema import SectionSchema
from models.grade import Grade
from models.year import Year
from tests.test_api.dynamic_schema import DynamicSchema
from tests.typing import Credential

from tests.test_api._helpers import _validate_invalid_fields_response


class TestSectionsApi:
    @pytest.mark.parametrize(
        "test_case, fields, expected_status",
        [
            ("no_fields", None, 200),
            (
                "valid_fields",
                random.sample(
                    list(SectionSchema.model_fields.keys()),
                    k=random.randint(1, len(SectionSchema.model_fields.keys())),
                ),
                200,
            ),
            (
                "invalid_fields",
                list(
                    set(
                        random.sample(
                            list(SectionSchema.model_fields.keys()),
                            k=random.randint(1, len(SectionSchema.model_fields.keys())),
                        )
                        + ["invalid1", "invalid2"]
                    )
                ),
                400,
            ),
        ],
        ids=["no-fields", "valid-fields", "invalid-fields"],
    )
    def test_get_sections(
        self,
        academic_year: Year,
        client: FlaskClient,
        random_auth_header: Credential,
        test_case: str,
        fields: list[str] | None,
        expected_status: int,
    ) -> None:
        """Test the API endpoint for retrieving all grades with various field selections."""
        url = f"/api/v1/years/{academic_year.id}/sections"
        if fields:
            url += f"?fields={','.join(fields)}"

        response = client.get(url, headers=random_auth_header["header"])

        assert response.status_code == expected_status
        assert response.json is not None

        if expected_status == 200:
            expected_fields = (
                fields if fields is not None else list(SectionSchema.default_fields())
            )
            DynamicSchema.validate_response(
                response_data=response.json,
                base_model=SectionSchema,
                expected_fields=expected_fields,
                type="list",
            )
        elif expected_status == 400:
            allowed_fields = set(SectionSchema.model_fields.keys())
            invalid_fields = set(fields if fields else []) - allowed_fields
            _validate_invalid_fields_response(response.json, invalid_fields)

    # def test_get_section_for_student_term(
    #     self,
    #     client: FlaskClient,
    #     student_terms: List[StudentTermRecord],
    #     random_auth_header: Credential,
    # ) -> None:
    #     """Test the API endpoint for retrieving sections for a specific student term."""
    #     student_term_id = random.choice(student_terms).id
    #     url = f"/api/v1/student_term/{student_term_id}/sections"

    #     response = client.get(url, headers=random_auth_header["header"])

    #     assert response.status_code == 200
    #     assert response.json is not None

    @pytest.mark.parametrize(
        "test_case, fields, expected_status",
        [
            ("no_fields", None, 200),
            (
                "valid_fields",
                random.sample(
                    list(SectionSchema.model_fields.keys()),
                    k=random.randint(1, len(SectionSchema.model_fields.keys())),
                ),
                200,
            ),
            (
                "invalid_fields",
                list(
                    set(
                        random.sample(
                            list(SectionSchema.model_fields.keys()),
                            k=random.randint(1, len(SectionSchema.model_fields.keys())),
                        )
                        + ["invalid1", "invalid2"]
                    )
                ),
                400,
            ),
        ],
        ids=["no-fields", "valid-fields", "invalid-fields"],
    )
    def test_get_section_for_grade(
        self,
        client: FlaskClient,
        grades: List[Grade],
        random_auth_header: Credential,
        test_case: str,
        fields: list[str] | None,
        expected_status: int,
    ) -> None:
        """Test the API endpoint for retrieving sections for a specific grade."""
        grade_id = random.choice(grades).id
        url = f"/api/v1/grades/{grade_id}/sections"
        if fields:
            url += f"?fields={','.join(fields)}"

        response = client.get(url, headers=random_auth_header["header"])

        assert response.status_code == expected_status
        assert response.json is not None

        if expected_status == 200:
            expected_fields = (
                fields if fields is not None else list(SectionSchema.default_fields())
            )
            DynamicSchema.validate_response(
                response_data=response.json,
                base_model=SectionSchema,
                expected_fields=expected_fields,
                type="list",
            )
        elif expected_status == 400:
            allowed_fields = set(SectionSchema.model_fields.keys())
            invalid_fields = set(fields if fields else []) - allowed_fields
            _validate_invalid_fields_response(response.json, invalid_fields)

    @pytest.mark.parametrize(
        "test_case, fields, expected_status",
        [
            ("no_fields", None, 200),
            (
                "valid_fields",
                random.sample(
                    list(SectionSchema.model_fields.keys()),
                    k=random.randint(1, len(SectionSchema.model_fields.keys())),
                ),
                200,
            ),
            (
                "invalid_fields",
                list(
                    set(
                        random.sample(
                            list(SectionSchema.model_fields.keys()),
                            k=random.randint(1, len(SectionSchema.model_fields.keys())),
                        )
                        + ["invalid1", "invalid2"]
                    )
                ),
                400,
            ),
        ],
        ids=["no-fields", "valid-fields", "invalid-fields"],
    )
    def test_get_section_by_id(
        self,
        client: FlaskClient,
        sections: List[SectionSchema],
        random_auth_header: Credential,
        test_case: str,
        fields: list[str] | None,
        expected_status: int,
    ) -> None:
        """Test the API endpoint for retrieving a single grade by ID with various field selections."""
        section_id = random.choice(sections).id
        url = f"/api/v1/sections/{section_id}"
        if fields:
            url += f"?fields={','.join(fields)}"

        response = client.get(url, headers=random_auth_header["header"])

        assert response.status_code == expected_status
        assert response.json is not None

        if expected_status == 200:
            expected_fields = (
                fields if fields is not None else list(SectionSchema.default_fields())
            )
            DynamicSchema.validate_response(
                response_data=response.json,
                base_model=SectionSchema,
                expected_fields=expected_fields,
            )
        elif expected_status == 400:
            allowed_fields = set(SectionSchema.model_fields.keys())
            invalid_fields = set(fields if fields else []) - allowed_fields
            _validate_invalid_fields_response(response.json, invalid_fields)

    def test_get_sections_unauthorized(
        self,
        client: FlaskClient,
        academic_year: Year,
    ) -> None:
        """Test that a 401 error is returned when no auth header is provided."""
        url = f"/api/v1/years/{academic_year.id}/sections"
        response = client.get(url)

        assert response.status_code == 401

    def test_get_section_by_id_unauthorized(
        self,
        client: FlaskClient,
        sections: List[SectionSchema],
    ) -> None:
        """Test that a 401 error is returned when no auth header is provided."""
        section_id = random.choice(sections).id
        url = f"/api/v1/sections/{section_id}"
        response = client.get(url)

        assert response.status_code == 401

    def test_get_section_by_id_not_found(
        self,
        client: FlaskClient,
        random_auth_header: Credential,
    ) -> None:
        """Test that a 404 error is returned for a non-existent section ID."""
        non_existent_section_id = 99999  # An ID that is unlikely to exist
        url = f"/api/v1/sections/{non_existent_section_id}"
        response = client.get(url, headers=random_auth_header["header"])

        assert response.status_code == 404
