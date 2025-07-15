from typing import Any, Dict, Optional
from flask import Blueprint, Response
import logging
from pydantic_core import ErrorDetails
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

from extension.pydantic.response.schema import ValidationErrorSchema, error_response

errors = Blueprint("errors", __name__)

# Configure logging
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)


@errors.app_errorhandler(SQLAlchemyError)
def handle_database_error(
    message: str = "Database Error",
    error: Optional[SQLAlchemyError] = None,
) -> tuple[Response, int]:
    """
    Handle database-related errors.
    """
    logging.error(f"{message}: {error}")
    return error_response(
        message=str(message),
        status=500,
    )


@errors.app_errorhandler(ValidationError)
def handle_validation_error(error: ValidationError) -> tuple[Response, int]:
    """
    Handles Pydantic's ValidationError.

    Returns a 422 Unprocessable Entity response with a structured
    JSON body detailing the validation errors.
    """
    logging.error(f"Validation Error: {error}")

    def format_error(err: ErrorDetails) -> Dict[str, Any]:
        """Format a single Pydantic error into a more readable structure."""
        formatted_err: Dict[str, Any] = {
            "location": ".".join(map(str, err.get("loc", []))),
            "message": err.get("msg", "Unknown error"),
            "input": err.get("input", None),
            "expected_type": err.get("type", "unknown"),
        }
        ctx = err.get("ctx")
        if ctx and "expected" in ctx:
            formatted_err["expected"] = ctx["expected"]

        validation_schema = ValidationErrorSchema.model_validate(formatted_err)
        formatted_err_schema = validation_schema.model_dump(
            exclude_none=True, by_alias=True, mode="json"
        )
        return formatted_err_schema

    try:
        formatted_errors = [format_error(err) for err in error.errors()]
        return error_response(
            message="Validation Error", status=422, meta=formatted_errors
        )
    except Exception as e:
        logging.error(f"Failed to parse Pydantic validation errors: {e}")
        # Fallback for unexpected error formatting issues
        return error_response(message="Validation Error", status=422)


@errors.app_errorhandler(ValueError)
def handle_value_error(error: ValueError) -> tuple[Response, int]:
    """
    Handle ValueError exceptions.
    """
    logging.error(f"Value Error: {error}")
    return error_response(
        message="Value Error",
        status=500,
    )


@errors.app_errorhandler(500)
def handle_internal_error(
    message: str = "Internal Server Error",
    error: Optional[Exception] = None,
) -> tuple[Response, int]:
    logging.error(f"handle_internal_error => {message}: {error}")
    return error_response(
        message=str(message),
        status=500,
    )


@errors.app_errorhandler(404)
def handle_not_found_error(
    message: str = "Not Found Error",
    error: Optional[Exception] = None,
) -> tuple[Response, int]:
    logging.error(f"{message}: {error}")
    return error_response(
        message=str(message),
        status=404,
    )


@errors.app_errorhandler(401)
def handle_invalid_credentials_error(
    message: str = "Invalid credentials",
    error: Optional[Exception] = None,
) -> tuple[Response, int]:
    logging.error(f"{message}: {error}")
    return error_response(
        message=str(message),
        status=401,
    )
