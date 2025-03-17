#!/usr/bin/python3
"""Utility functions for the API"""

import jwt
import uuid
from datetime import datetime, timedelta
from flask import current_app  # Import current_app to access app context
from functools import wraps
from flask import request, jsonify
from models.student import Student
from models import storage
from models.stud_year_record import STUDYearRecord
from models.teacher import Teacher
from sqlalchemy import func
from models import storage
from models.user import User
from models.admin import Admin
from models.mark_list import MarkList
from models.stud_semester_record import STUDSemesterRecord
from models.blacklist_token import BlacklistToken


def create_token(user_id, role):
    """
    Generate a JWT token for a user based on their role.

    Args:
        user_id (int): The unique identifier of the user.
        role (str): The role of the user (e.g., 'admin', 'teacher', 'student').

    Returns:
        str: A JWT token encoded with the user's ID, expiration time, role, and a unique JTI.

    The token expires in 720 minutes (12 hours) from the time of creation.
    """
    # Determine the secret key based on the role
    secret_keys = {
        'admin': current_app.config["ADMIN_SECRET_KEY"],
        'teacher': current_app.config["TEACHER_SECRET_KEY"],
        'student': current_app.config["STUDENT_SECRET_KEY"],
    }
    secret_key = secret_keys.get(role)
    if not secret_key:
        raise ValueError(f"Invalid role: {role}")

    # Create the payload
    payload = {
        'id': user_id,
        'exp': datetime.utcnow() + timedelta(minutes=720),  # 12 hours expiration
        'role': role,
        'jti': str(uuid.uuid4())  # Unique token identifier
    }

    # Encode and return the token
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def check_blacklist_token(token):
    # Check if the token is blacklisted
    try:
        # Decode the token without verifying the signature to get the JTI
        unverified_payload = jwt.decode(
            token, options={"verify_signature": False})
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


def decode_and_retrieve_user(token, secret_key):
    """Helper function to decode token and retrieve user data"""
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        user_data = storage.get_first(
            User, identification=payload['id'])
        if user_data:
            return user_data
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return None
    return None


# Decorator for Admin JWT verification
def admin_required(f):
    """
    Decorator to ensure that the request is made by an authenticated admin user.

    This decorator checks for the presence of a valid JWT token in the 'apiKey' header of the request.
    The token is expected to be in the format 'Bearer <token>'. The token is then decoded using the secret key
    specified in the application's configuration. If the token is valid and corresponds to an existing admin user,
    the decorated function is called with the admin data passed as the first argument.

    Args:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function which includes the admin data if the token is valid.

    Raises:
        401 Unauthorized: If the token is missing, expired, or invalid.
        404 Not Found: If the token is valid but the admin user does not exist.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'apiKey' in request.headers:
            token = request.headers['apiKey'].split()[1]  # Bearer token

        if not token:
            return jsonify({"error": "Unauthorized", "reason": "UNAUTHORIZED"}), 401

        # Check if the token is blacklisted
        is_blacklisted, error_message = check_blacklist_token(token)
        if is_blacklisted:
            return jsonify({'message': error_message}), 401

        admin_data = decode_and_retrieve_user(
            token, current_app.config["ADMIN_SECRET_KEY"])
        if admin_data:
            return f(admin_data, *args, **kwargs)

        return jsonify({'message': 'Unauthorized access'}), 401

    return decorated_function


# Decorator for teacher JWT verification
def teacher_required(f):
    """
    Decorator to ensure that the request is made by an authenticated teacher.

    This decorator checks for the presence of a JWT token in the 'apiKey' header of the request.
    The token is expected to be in the format 'Bearer <token>'. The token is then decoded using the 
    secret key specified in the application's configuration. If the token is valid and corresponds 
    to an existing teacher, the decorated function is called with the teacher's data passed as the 
    first argument. If the token is missing, expired, invalid, or the teacher is not found, an 
    appropriate JSON response with an error message and status code is returned.

    Args:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function with teacher authentication enforced.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'apiKey' in request.headers:
            token = request.headers['apiKey'].split()[1]  # Bearer token

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        # Check if the token is blacklisted
        is_blacklisted, error_message = check_blacklist_token(token)
        if is_blacklisted:
            return jsonify({'message': error_message}), 401

        teacher_data = decode_and_retrieve_user(
            token, current_app.config["TEACHER_SECRET_KEY"])

        if teacher_data:
            return f(teacher_data, *args, **kwargs)

        return jsonify({'message': 'Unauthorized access'}), 401

    return decorated_function


# Decorator for student JWT verification
def student_required(f):
    """
    Decorator to ensure that the request is made by an authenticated student.

    This decorator checks for the presence of a JWT token in the 'apiKey' header of the request.
    It decodes the token using the student secret key and retrieves the student data from the storage.
    If the token is missing, expired, invalid, or if the student is not found, it returns an appropriate
    JSON response with a corresponding HTTP status code.

    Args:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function which includes the student data as the first argument.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'apiKey' in request.headers:
            token = request.headers['apiKey'].split()[1]  # Bearer token

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        # Check if the token is blacklisted
        is_blacklisted, error_message = check_blacklist_token(token)
        if is_blacklisted:
            return jsonify({'message': error_message}), 401

        # Try decoding as a student token
        student_data = decode_and_retrieve_user(
            token, current_app.config["STUDENT_SECRET_KEY"])
        if student_data:
            return f(student_data, *args, **kwargs)

        return jsonify({'message': 'Unauthorized access'}), 401

    return decorated_function


def admin_or_student_required(f):
    """
    Decorator to ensure that the request is made by either a student or an admin.

    This decorator checks the 'apiKey' header for a Bearer token and attempts to decode it
    using either the student or admin secret keys. If the token is valid and corresponds to a student,
    the decorated function is called with the student data and None for admin data. If the token is valid
    and corresponds to an admin, the decorated function is called with None for student data and the admin data.
    If the token is missing, expired, or invalid, an appropriate JSON response with a 401 status code is returned.

    Args:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function with student or admin data passed as arguments.

    Raises:
        401 Unauthorized: If the token is missing, expired, or invalid.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'apiKey' in request.headers:
            token = request.headers['apiKey'].split()[1]  # Bearer token

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        # Check if the token is blacklisted
        is_blacklisted, error_message = check_blacklist_token(token)
        if is_blacklisted:
            return jsonify({'message': error_message}), 401

        # Try decoding as an admin token
        admin_data = decode_and_retrieve_user(
            token, current_app.config["ADMIN_SECRET_KEY"])
        if admin_data:
            return f(admin_data, None, *args, **kwargs)

        # Try decoding as a student token
        student_data = decode_and_retrieve_user(
            token, current_app.config["STUDENT_SECRET_KEY"])
        if student_data:
            return f(None, student_data, *args, **kwargs)

        return jsonify({'message': 'Unauthorized access'}), 401

    return decorated_function


# Unified decorator for Student and Admin JWT verification
def student_teacher_or_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'apiKey' in request.headers:
            token = request.headers['apiKey'].split()[1]  # Bearer token

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        # Check if the token is blacklisted
        is_blacklisted, error_message = check_blacklist_token(token)
        if is_blacklisted:
            return jsonify({'message': error_message}), 401

        # Try decoding as a student token
        student_data = decode_and_retrieve_user(
            token, current_app.config["STUDENT_SECRET_KEY"])
        if student_data:
            return f(student_data, None, None, *args, **kwargs)

        # Try decoding as a teacher token
        teacher_data = decode_and_retrieve_user(
            token, current_app.config["TEACHER_SECRET_KEY"])
        if teacher_data:
            return f(None, teacher_data, None, *args, **kwargs)

        # Try decoding as an admin token
        admin_data = decode_and_retrieve_user(
            token, current_app.config["ADMIN_SECRET_KEY"])
        if admin_data:
            return f(None, None, admin_data, *args, **kwargs)

        return jsonify({'message': 'Unauthorized access'}), 401

    return decorated_function
