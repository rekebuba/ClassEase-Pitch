#!/usr/bin/python3
"""Public views module for the API"""

from typing import Tuple, Optional
import jwt
from flask import Response, request, jsonify
from api.v1.views.utils import create_token, student_teacher_or_admin_required
from marshmallow import ValidationError
from api.v1.utils.typing import AuthType, UserT
from api.v1.views.shared import auths as auth
from models import storage
from models.blacklist_token import BlacklistToken
from api.v1.views.shared.auth.schema import AuthSchema, InvalidCredentialsError
from api.v1.views import errors


@auth.route("auth/login", methods=["POST"])
def login() -> Tuple[Response, int]:
    """
    Handle user login by validating credentials and generating an access token.
    """
    try:
        auth_schema = AuthSchema()
        valid_user: AuthType = auth_schema.load(request.get_json())

        # Generate an api_key token based on the user's role
        api_key = create_token(valid_user["identification"], valid_user["role"])

        return auth_schema.dump(
            {
                "message": "logged in successfully.",
                "api_key": api_key,
                "role": valid_user["role"],
            }
        ), 200
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except InvalidCredentialsError as e:
        return errors.handle_invalid_credentials_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)


@auth.route("auth/logout", methods=["POST"])
@student_teacher_or_admin_required
def logout(user: UserT) -> Tuple[Response, int]:
    token: str = request.headers["apiKey"].split()[1]  # Extract the token
    try:
        # Decode the token to get the JTI
        payload = jwt.decode(token, options={"verify_signature": False})
        jti: Optional[str] = payload.get("jti")

        if not jti:
            raise Exception

        # Add the JTI to the blacklist table
        black_list = BlacklistToken(jti=jti)
        storage.add(black_list)

        return jsonify({"message": "Successfully logged out"}), 200
    except Exception as e:
        return errors.handle_internal_error(e)
