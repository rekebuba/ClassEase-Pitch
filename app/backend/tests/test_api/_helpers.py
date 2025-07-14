from typing import Any, Dict, Set
import pytest
from pydantic import ValidationError

from api.v1.utils.parameter import InvalidFieldsResponse
from extension.pydantic.response.schema import ErrorResponseSchema


def _validate_invalid_fields_response(
    response: Dict[str, Any], invalid_fields: Set[str]
) -> None:
    """Helper function to validate a 400 Bad Request response for invalid fields."""
    try:
        validated_error = ErrorResponseSchema[
            InvalidFieldsResponse, None
        ].model_validate(response)
        assert validated_error.meta is not None
        assert set(validated_error.meta.invalid_fields) == invalid_fields
    except ValidationError as e:
        pytest.fail(f"Validation error for wrong fields: {e}")
