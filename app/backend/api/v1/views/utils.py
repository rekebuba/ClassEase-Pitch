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


# Function to generate JWT for Admins
def create_admin_token(admin_id):
    """
    Generate a JWT token for an admin user.

    Args:
        admin_id (int): The unique identifier of the admin user.

    Returns:
        str: A JWT token encoded with the admin's ID, expiration time, and role.

    The token expires in 30 minutes from the time of creation.
    """
    payload = {
        'id': admin_id,
        'exp': datetime.utcnow() + timedelta(minutes=720),
        'role': 'admin',
        "jti": str(uuid.uuid4())
    }
    token = jwt.encode(
        payload, current_app.config["ADMIN_SECRET_KEY"], algorithm="HS256")
    return token


# Function to generate JWT for teachers
def create_teacher_token(teacher_id):
    """
    Generate a JWT token for a teacher.

    Args:
        teacher_id (int): The unique identifier of the teacher.

    Returns:
        str: A JWT token encoded with the teacher's information and expiration time.

    The token payload includes:
        - 'id': The teacher's unique identifier.
        - 'exp': The expiration time of the token, set to 15 minutes from the current time.
        - 'role': The role of the user, set to 'teacher'.
    """
    payload = {
        'id': teacher_id,
        'exp': datetime.utcnow() + timedelta(minutes=720),
        'role': 'teacher',
        "jti": str(uuid.uuid4())
    }
    token = jwt.encode(
        payload, current_app.config["TEACHER_SECRET_KEY"], algorithm="HS256")
    return token


# Function to generate JWT for students
def create_student_token(student_id):
    """
    Generate a JWT token for a student.

    Args:
        student_id (int): The unique identifier of the student.

    Returns:
        str: A JWT token encoded with the student's information and expiration time.
    """
    payload = {
        'id': student_id,
        'exp': datetime.utcnow() + timedelta(minutes=720),
        'role': 'student',
        "jti": str(uuid.uuid4())
    }
    token = jwt.encode(
        payload, current_app.config["STUDENT_SECRET_KEY"], algorithm="HS256")
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


# Decorator for Admin JWT verification
def admin_required(f):
    """
    Decorator to ensure that the request is made by an authenticated admin user.

    This decorator checks for the presence of a valid JWT token in the 'Authorization' header of the request.
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
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]  # Bearer token

        if not token:
            return jsonify({"error": "Unauthorized", "reason": "UNAUTHORIZED"}), 401

        # Check if the token is blacklisted
        is_blacklisted, error_message = check_blacklist_token(token)
        if is_blacklisted:
            return jsonify({'message': error_message}), 401

        try:
            payload = jwt.decode(
                token, current_app.config["ADMIN_SECRET_KEY"], algorithms=["HS256"])
            admin_data = storage.get_first(User, identification=payload['id'])
            if not admin_data:
                return jsonify({"error": "Unauthorized", "reason": "UNAUTHORIZED"}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Unauthorized", "reason": "SESSION_EXPIRED"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Unauthorized", "reason": "Invalid Token"}), 401

        return f(admin_data, *args, **kwargs)

    return decorated_function


# Decorator for teacher JWT verification
def teacher_required(f):
    """
    Decorator to ensure that the request is made by an authenticated teacher.

    This decorator checks for the presence of a JWT token in the 'Authorization' header of the request.
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
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]  # Bearer token

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        # Check if the token is blacklisted
        is_blacklisted, error_message = check_blacklist_token(token)
        if is_blacklisted:
            return jsonify({'message': error_message}), 401

        try:
            payload = jwt.decode(
                token, current_app.config["TEACHER_SECRET_KEY"], algorithms=["HS256"])
            teacher_data = storage.get_first(
                User, identification=payload['id'])
            if not teacher_data:
                return jsonify({'message': 'Teacher not found!'}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Teacher token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid Teacher token'}), 401

        return f(teacher_data, *args, **kwargs)

    return decorated_function


# Decorator for student JWT verification
def student_required(f):
    """
    Decorator to ensure that the request is made by an authenticated student.

    This decorator checks for the presence of a JWT token in the 'Authorization' header of the request.
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
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]  # Bearer token

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        # Check if the token is blacklisted
        is_blacklisted, error_message = check_blacklist_token(token)
        if is_blacklisted:
            return jsonify({'message': error_message}), 401

        try:
            payload = jwt.decode(
                token, current_app.config["STUDENT_SECRET_KEY"], algorithms=["HS256"])
            student_data = storage.get_first(
                User, identification=payload['id'])
            if not student_data:
                return jsonify({'message': 'Student not found!'}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Student token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid Student token'}), 401

        return f(student_data, *args, **kwargs)

    return decorated_function


def admin_or_student_required(f):
    """
    Decorator to ensure that the request is made by either a student or an admin.

    This decorator checks the 'Authorization' header for a Bearer token and attempts to decode it
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
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]  # Bearer token

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        # Check if the token is blacklisted
        is_blacklisted, error_message = check_blacklist_token(token)
        if is_blacklisted:
            return jsonify({'message': error_message}), 401

        try:
            # First, try decoding as an admin token
            payload = jwt.decode(
                token, current_app.config["ADMIN_SECRET_KEY"], algorithms=["HS256"])
            admin_data = storage.get_first(Admin, id=payload['id'])
            if admin_data:
                return f(admin_data, None, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            pass  # Invalid for student, let's check for admin

        try:
            # Then, try decoding as a student token
            payload = jwt.decode(
                token, current_app.config["STUDENT_SECRET_KEY"], algorithms=["HS256"])
            student_data = storage.get_first(
                STUDYearRecord, student_id=payload['id'])
            if student_data:
                return f(None, student_data, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return jsonify({'message': 'Unauthorized access'}), 401

    return decorated_function


# Unified decorator for Student and Admin JWT verification
def student_teacher_or_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]  # Bearer token

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        # Check if the token is blacklisted
        is_blacklisted, error_message = check_blacklist_token(token)
        if is_blacklisted:
            return jsonify({'message': error_message}), 401

        try:
            # First, try decoding as a student token
            payload = jwt.decode(
                token, current_app.config["STUDENT_SECRET_KEY"], algorithms=["HS256"])
            student_data = storage.get_first(
                STUDYearRecord, student_id=payload['id'])
            if student_data:
                return f(student_data, None, None, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            pass  # Invalid for student, let's check for admin

        try:
            # Then, try decoding as an teacher token
            payload = jwt.decode(
                token, current_app.config["TEACHER_SECRET_KEY"], algorithms=["HS256"])
            teacher_data = storage.get_first(Teacher, id=payload['id'])
            if teacher_data:
                return f(None, teacher_data, None, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            pass  # Invalid for teacher, let's check for admin

        try:
            # try decoding as an admin token
            payload = jwt.decode(
                token, current_app.config["ADMIN_SECRET_KEY"], algorithms=["HS256"])
            admin_data = storage.get_first(Admin, id=payload['id'])
            if admin_data:
                return f(None, None, admin_data, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return jsonify({'message': 'Unauthorized access'}), 401

    return decorated_function
