from typing import Optional
from flask import Blueprint, Response
import logging
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

from extension.pydantic.response.schema import error_response

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
        message=message,
        status=500,
    )


@errors.errorhandler(ValidationError)
def handle_validation_error(
    message: str = "Validation Error",
    error: Optional[ValidationError] = None,
) -> tuple[Response, int]:
    logging.error(f"{message}: {error}")  # Log the error (not shown to user)
    return error_response(
        message=message,
        status=422,
    )


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
    logging.error(f"{message}: {error}")
    return error_response(
        message=message,
        status=500,
    )


@errors.app_errorhandler(404)
def handle_not_found_error(
    message: str = "Not Found Error",
    error: Optional[Exception] = None,
) -> tuple[Response, int]:
    logging.error(f"{message}: {error}")
    return error_response(
        message=message,
        status=404,
    )


@errors.app_errorhandler(401)
def handle_invalid_credentials_error(
    message: str = "Invalid credentials",
    error: Optional[Exception] = None,
) -> tuple[Response, int]:
    logging.error(f"{message}: {error}")
    return error_response(
        message=message,
        status=401,
    )
