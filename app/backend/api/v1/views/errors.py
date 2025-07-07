from typing import Union
from flask import Blueprint, Response, jsonify
import logging
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

errors = Blueprint("errors", __name__)

# Configure logging
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)


@errors.app_errorhandler(SQLAlchemyError)
def handle_database_error(error: SQLAlchemyError) -> tuple[Response, int]:
    """
    Handle database-related errors.
    """
    logging.error(f"Database Error: {error}")
    return jsonify({"message": "Database error Try Again in a moment"}), 500


@errors.errorhandler(ValidationError)
def handle_validation_error(error: ValidationError) -> tuple[Response, int]:
    logging.error(f"Validation Error: {error}")  # Log the error (not shown to user)
    return jsonify(
        {
            "message": "Validation error",
            "errors": error.errors(),  # Pydantic-style error details
        }
    ), 422  # HTTP 422 Unprocessable Entity


@errors.app_errorhandler(ValueError)
def handle_value_error(error: ValueError) -> tuple[Response, int]:
    """
    Handle ValueError exceptions.
    """
    logging.error(f"Value Error: {error}")
    return jsonify({"message": "Invalid input", "error": str(error)}), 400


@errors.app_errorhandler(500)
def handle_internal_error(error: Union[Exception, str]) -> tuple[Response, int]:
    logging.error(f"Internal Server Error: {error}")
    return jsonify({"message": "Internal server error", "error": str(error)}), 500


@errors.app_errorhandler(404)
def handle_not_found_error(error: Union[Exception, str]) -> tuple[Response, int]:
    logging.error(f"Not Found Error: {error}")
    return jsonify({"message": "Resource not found", "error": str(error)}), 404


@errors.app_errorhandler(401)
def handle_invalid_credentials_error(
    error: Union[Exception, str],
) -> tuple[Response, int]:
    logging.error(f"Invalid Credentials Error: {error}")
    return jsonify({"message": "Invalid credentials", "error": str(error)}), 401
