#!/usr/bin/python3
"""Public views module for the API"""

from flask import Blueprint, request, jsonify
from api.v1.views.utils import create_student_token, create_teacher_token, create_admin_token
from models import storage
from models.users import User

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


@app_views.route('/login', methods=['POST'])
def login():
    """
    Handle user login by validating credentials and generating an access token.

    This function extracts the 'id' and 'password' from the query parameters of the request URL.
    It checks if the required fields are present and validates the user's credentials.
    If the credentials are valid, it generates an access token based on the user's role
    (Student, Teacher, or Admin) and returns it in the response.

    Returns:
        Response: A JSON response containing the access token and user role if the credentials are valid.
                  A JSON response with an error message and appropriate status code if the credentials are invalid
                  or if required fields are missing.

    Status Codes:
        200: Successful login with valid credentials.
        400: Missing 'id' or 'password' in the request.
        401: Invalid credentials or invalid user role.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    required_fields = {'id', 'password'}
    for field in required_fields:
        if field not in data:
            return jsonify({"error": "Missing id or password"}), 400

    if 'id' not in data or 'password' not in data:
        return jsonify({"error": "Missing id or password"}), 400

    print(data)
    user = storage.get_first(User, id=data['id'])
    if user and user.check_password(data['password']):
        if user.role == 'Student':
            access_token = create_student_token(user.id)
        elif user.role == 'Teacher':
            access_token = create_teacher_token(user.id)
        elif user.role == 'Admin':
            access_token = create_admin_token(user.id)
        else:
            return jsonify({"error": "Invalid role"}), 401
        return jsonify(access_token=access_token, role=user.role), 200

    return jsonify({"error": "Invalid credentials"}), 401
