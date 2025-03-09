#!/usr/bin/python3
"""Public views module for the API"""

import jwt
from flask import Blueprint, request, jsonify
from api.v1.views.utils import create_student_token, create_teacher_token, create_admin_token, student_teacher_or_admin_required
from marshmallow import ValidationError
from models import storage
from models.user import User
from models.blacklist_token import BlacklistToken
from api.v1.schemas.user.auth_schema import AuthSchema, InvalidCredentialsError
from api.v1.views import errors
from api.v1.services.user_service import UserService

auth = Blueprint('auth', __name__, url_prefix='/api/v1')


@auth.route('auth/login', methods=['POST'])
def login():
    """
    Handle user login by validating credentials and generating an access token.
    """
    try:
        auth_schema = AuthScwwhema()
        valid_user = auth_schema.load(request.get_json())

        # Generate an api_key token based on the user's role
        api_key = UserService.generate_api_key(
            valid_user['role'], valid_user['identification'])

        return auth_schema.dump({"message": "logged in successfully.", "api_key": api_key}), 200
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except InvalidCredentialsError as e:
        return errors.handle_invalid_credentials_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)


@auth.route("/auth/logout", methods=["POST"])
@student_teacher_or_admin_required
def logout(student, teacher, admin):
    token = request.headers['api_key'].split()[1]  # Extract the token
    try:
        # Decode the token to get the JTI
        payload = jwt.decode(token, options={"verify_signature": False})
        jti = payload.get("jti")

        print(jti)
        # Add the JTI to the blacklist table
        black_list = BlacklistToken(jti=jti)
        storage.add(black_list)

        return jsonify({'message': 'Successfully logged out'}), 200
    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Logout failed', 'error': str(e)}), 500
