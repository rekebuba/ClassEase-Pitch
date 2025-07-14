import random
from typing import List
import pytest
from flask.testing import FlaskClient
from extension.pydantic.models.stream_schema import StreamSchema
from models.year import Year
from tests.test_api.dynamic_schema import DynamicSchema
from tests.typing import Credential

from tests.test_api._helpers import _validate_invalid_fields_response


class TestStreamsApi:
    @pytest.mark.parametrize(
        "test_case, fields, expected_status",
        [
            ("no_fields", None, 200),
            (
                "valid_fields",
                random.sample(
                    list(StreamSchema.model_fields.keys()),
                    k=random.randint(1, len(StreamSchema.model_fields.keys())),
                ),
                200,
            ),
            (
                "invalid_fields",
                list(
                    set(
                        random.sample(
                            list(StreamSchema.model_fields.keys()),
                            k=random.randint(1, len(StreamSchema.model_fields.keys())),
                        )
                        + ["invalid1", "invalid2"]
                    )
                ),
                400,
            ),
        ],
        ids=["no-fields", "valid-fields", "invalid-fields"],
    )
    def test_get_streams(
        self,
        academic_year: Year,
        client: FlaskClient,
        random_auth_header: Credential,
        test_case: str,
        fields: list[str] | None,
        expected_status: int,
    ) -> None:
        """Test the API endpoint for retrieving all streams with various field selections."""
        url = f"/api/v1/years/{academic_year.id}/streams"
        if fields:
            url += f"?fields={','.join(fields)}"

        response = client.get(url, headers=random_auth_header["header"])

        assert response.status_code == expected_status
        assert response.json is not None

        if expected_status == 200:
            expected_fields = (
                fields if fields is not None else StreamSchema.default_fields()
            )
            DynamicSchema.validate_response(
                response_data=response.json,
                base_model=StreamSchema,
                expected_fields=expected_fields,
                type="list",
            )
        elif expected_status == 400:
            allowed_fields = set(StreamSchema.model_fields.keys())
            invalid_fields = set(fields if fields else []) - allowed_fields
            _validate_invalid_fields_response(response.json, invalid_fields)

    @pytest.mark.parametrize(
        "test_case, fields, expected_status",
        [
            ("no_fields", None, 200),
            (
                "valid_fields",
                random.sample(
                    list(StreamSchema.model_fields.keys()),
                    k=random.randint(1, len(StreamSchema.model_fields.keys())),
                ),
                200,
            ),
            (
                "invalid_fields",
                list(
                    set(
                        random.sample(
                            list(StreamSchema.model_fields.keys()),
                            k=random.randint(1, len(StreamSchema.model_fields.keys())),
                        )
                        + ["invalid1", "invalid2"]
                    )
                ),
                400,
            ),
        ],
        ids=["no-fields", "valid-fields", "invalid-fields"],
    )
    def test_get_stream_by_id(
        self,
        academic_year: Year,
        client: FlaskClient,
        streams: List[StreamSchema],
        random_auth_header: Credential,
        test_case: str,
        fields: list[str] | None,
        expected_status: int,
    ) -> None:
        """Test the API endpoint for retrieving a single grade by ID with various field selections."""
        stream_id = random.choice(streams).id
        url = f"/api/v1/years/{academic_year.id}/streams/{stream_id}"
        if fields:
            url += f"?fields={','.join(fields)}"

        response = client.get(url, headers=random_auth_header["header"])

        assert response.status_code == expected_status
        assert response.json is not None

        if expected_status == 200:
            expected_fields = (
                fields if fields is not None else StreamSchema.default_fields()
            )
            DynamicSchema.validate_response(
                response_data=response.json,
                base_model=StreamSchema,
                expected_fields=expected_fields,
            )
        elif expected_status == 400:
            allowed_fields = set(StreamSchema.model_fields.keys())
            invalid_fields = set(fields if fields else []) - allowed_fields
            _validate_invalid_fields_response(response.json, invalid_fields)

    def test_get_streams_unauthorized(
        self,
        client: FlaskClient,
        academic_year: Year,
    ) -> None:
        """Test that a 401 error is returned when no auth header is provided."""
        url = f"/api/v1/years/{academic_year.id}/streams"
        response = client.get(url)

        assert response.status_code == 401

    def test_get_stream_by_id_unauthorized(
        self,
        client: FlaskClient,
        academic_year: Year,
        streams: List[StreamSchema],
    ) -> None:
        """Test that a 401 error is returned when no auth header is provided."""
        stream_id = random.choice(streams).id
        url = f"/api/v1/years/{academic_year.id}/streams/{stream_id}"
        response = client.get(url)

        assert response.status_code == 401

    def test_get_stream_by_id_not_found(
        self,
        client: FlaskClient,
        random_auth_header: Credential,
        academic_year: Year,
    ) -> None:
        """Test that a 404 error is returned for a non-existent stream ID."""
        non_existent_stream_id = 99999  # An ID that is unlikely to exist
        url = f"/api/v1/years/{academic_year.id}/streams/{non_existent_stream_id}"
        response = client.get(url, headers=random_auth_header["header"])

        assert response.status_code == 404
