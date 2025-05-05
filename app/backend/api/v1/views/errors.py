from flask import Blueprint, Response, jsonify
from marshmallow import ValidationError
import logging

errors = Blueprint("errors", __name__)

# Configure logging
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)


@errors.errorhandler(ValidationError)
def handle_validation_error(error: ValidationError) -> tuple[Response, int]:
    logging.error(f"Validation Error: {error}")  # Log the error (not shown to user)
    return jsonify(
        {
            "message": "Validation error",
            "errors": error.messages,  # Marshmallow provides error.messages
        }
    ), 400  # HTTP 400 Bad Request


@errors.app_errorhandler(500)
def handle_internal_error(error: Exception) -> tuple[Response, int]:
    logging.error(f"Internal Server Error: {error}")
    return jsonify({"message": "Internal server error", "error": str(error)}), 500


@errors.app_errorhandler(404)
def handle_not_found_error(error: Exception) -> tuple[Response, int]:
    logging.error(f"Not Found Error: {error}")
    return jsonify({"message": "Resource not found", "error": str(error)}), 404


@errors.app_errorhandler(401)
def handle_invalid_credentials_error(error: Exception) -> tuple[Response, int]:
    logging.error(f"Invalid Credentials Error: {error}")
    return jsonify({"message": "Invalid credentials", "error": str(error)}), 401
