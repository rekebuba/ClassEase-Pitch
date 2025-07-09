#!/usr/bin/python3
"""Utility functions for the API"""

import jwt
from typing import Any, Callable, Tuple, Union
from flask import Response, current_app  # Import current_app to access app context
from functools import wraps
from flask import request, jsonify
from api.v1.utils.typing import T
from models import storage
from models.user import User
from models.blacklist_token import BlacklistToken


def check_blacklist_token(token: str) -> Tuple[bool, str | None]:
    # Check if the token is blacklisted
    try:
        # Decode the token without verifying the signature to get the JTI
        unverified_payload = jwt.decode(token, options={"verify_signature": False})
        jti = unverified_payload.get("jti")  # Extract the JTI
        if not jti:
            return True, None

        # Query the blacklist table to check if the JTI is blacklisted
        result = storage.get_first(BlacklistToken, jti=jti)

        if result:
            return True, "Token is blacklisted. Please log in again."

        return False, None  # Token is not blacklisted
    except Exception as e:
        return True, f"Invalid token: {str(e)}"


def decode_and_retrieve_user(
    token: str, secret_key: str
) -> User | Tuple[Response, int] | None:
    """Helper function to decode token and retrieve user data"""
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        user_data = storage.get_first(User, identification=payload["id"])
        if user_data:
            return user_data
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return None
    return None


def admin_required(
    f: Callable[..., T],
) -> Callable[..., Union[T, Tuple[Response, int]]]:
    """
    Decorator to ensure that the request is made by an authenticated admin user.

    Args:
        f (function): The function to be decorated.

    Raises:
        401 Unauthorized: If the token is missing, expired, or invalid.
        404 Not Found: If the token is valid but the admin user does not exist.
    """

    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Union[T, Tuple[Response, int]]:
        """
        Decorated function to check for a valid token and retrieve user data.

        Returns:
            T: The decorated function with user data as the first argument.
        """
        if "apiKey" in request.headers:
            token = request.headers["apiKey"].split()[1]  # Bearer token

        if not token:
            return jsonify({"message": "Unauthorized Access. Please Login Again."}), 401

        # Check if the token is blacklisted
        is_blacklisted: bool
        error_message: Union[str, None]
        is_blacklisted, error_message = check_blacklist_token(token)
        if is_blacklisted:
            return jsonify({"message": error_message}), 401

        admin_data = decode_and_retrieve_user(
            token, current_app.config["ADMIN_SECRET_KEY"]
        )
        if admin_data:
            return f(admin_data, *args, **kwargs)

        return jsonify({"message": "Unauthorized Access. Please Login Again."}), 401

    return decorated_function


# Decorator for teacher JWT verification
def teacher_required(
    f: Callable[..., T],
) -> Callable[..., Union[T, Tuple[Response, int]]]:
    """
    Decorator to ensure that the request is made by an authenticated teacher.

    Args:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function with teacher authentication enforced.
    """

    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Union[T, Tuple[Response, int]]:
        """
        Decorated function to check for a valid token and retrieve user data.

        Returns:
            T: The decorated function with user data as the first argument.
        """
        if "apiKey" in request.headers:
            token = request.headers["apiKey"].split()[1]  # Bearer token

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        # Check if the token is blacklisted
        is_blacklisted: bool
        error_message: Union[str, None]
        is_blacklisted, error_message = check_blacklist_token(token)
        if is_blacklisted:
            jsonify({"message": error_message}), 401

        teacher_data = decode_and_retrieve_user(
            token, current_app.config["TEACHER_SECRET_KEY"]
        )

        if teacher_data:
            return f(teacher_data, *args, **kwargs)

        return jsonify({"message": "Unauthorized Access. Please Login Again."}), 401

    return decorated_function


# Decorator for student JWT verification
def student_required(
    f: Callable[..., T],
) -> Callable[..., Union[T, Tuple[Response, int]]]:
    """
    Decorator to ensure that the request is made by an authenticated student.

    Args:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function which includes the student data as the first argument.
    """

    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Union[T, Tuple[Response, int]]:
        """
        Decorated function to check for a valid token and retrieve user data.

        Returns:
            T: The decorated function with user data as the first argument.
        """
        if "apiKey" in request.headers:
            token = request.headers["apiKey"].split()[1]  # Bearer token

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        # Check if the token is blacklisted
        is_blacklisted: bool
        error_message: Union[str, None]
        is_blacklisted, error_message = check_blacklist_token(token)
        if is_blacklisted:
            jsonify({"message": error_message}), 401

        # Try decoding as a student token
        student_data = decode_and_retrieve_user(
            token, current_app.config["STUDENT_SECRET_KEY"]
        )
        if student_data:
            return f(student_data, *args, **kwargs)

        return jsonify({"message": "Unauthorized Access. Please Login Again."}), 401

    return decorated_function


def admin_or_student_required(
    f: Callable[..., T],
) -> Callable[..., Union[T, Tuple[Response, int]]]:
    """
    Decorator to ensure that the request is made by either a student or an admin.

    Args:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function with student or admin data passed as arguments.

    Raises:
        401 Unauthorized: If the token is missing, expired, or invalid.
    """

    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Union[T, Tuple[Response, int]]:
        """
        Decorated function to check for a valid token and retrieve user data.

        Returns:
            T: The decorated function with user data as the first argument.
        """
        if "apiKey" in request.headers:
            token = request.headers["apiKey"].split()[1]  # Bearer token

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        # Check if the token is blacklisted
        is_blacklisted: bool
        error_message: Union[str, None]
        is_blacklisted, error_message = check_blacklist_token(token)
        if is_blacklisted:
            jsonify({"message": error_message}), 401

        # Try decoding as an admin token
        admin_data = decode_and_retrieve_user(
            token, current_app.config["ADMIN_SECRET_KEY"]
        )
        if admin_data:
            return f(admin_data, *args, **kwargs)

        # Try decoding as a student token
        student_data = decode_and_retrieve_user(
            token, current_app.config["STUDENT_SECRET_KEY"]
        )
        if student_data:
            return f(student_data, *args, **kwargs)

        return jsonify({"message": "Unauthorized Access. Please Login Again."}), 401

    return decorated_function


# Unified decorator for Student and Admin JWT verification
def student_teacher_or_admin_required(
    f: Callable[..., T],
) -> Callable[..., Union[T, Tuple[Response, int]]]:
    """
    Decorator to ensure that the request is made by an authenticated student, teacher, or admin.

    Returns:
        function: The decorated function which includes the user data as the first argument.
    """

    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Union[T, Tuple[Response, int]]:
        """
        Decorated function to check for a valid token and retrieve user data.

        Returns:
            T: The decorated function with user data as the first argument.
        """
        if "apiKey" in request.headers:
            token = request.headers["apiKey"].split()[1]  # Bearer token

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        # Check if the token is blacklisted
        is_blacklisted, error_message = check_blacklist_token(token)
        if is_blacklisted:
            jsonify({"message": error_message}), 401

        # Try decoding as a student token
        user = decode_and_retrieve_user(token, current_app.config["STUDENT_SECRET_KEY"])

        if user:
            return f(user, *args, **kwargs)

        # Try decoding as a teacher token
        user = decode_and_retrieve_user(token, current_app.config["TEACHER_SECRET_KEY"])
        if user:
            return f(user, *args, **kwargs)

        # Try decoding as an admin token
        user = decode_and_retrieve_user(token, current_app.config["ADMIN_SECRET_KEY"])
        if user:
            return f(user, *args, **kwargs)

        return jsonify({"message": "Unauthorized Access. Please Login Again."}), 401

    return decorated_function
