#!/usr/bin/python3
"""Public views module for the API"""

from typing import Tuple, Optional
import jwt
from flask import Response, request, jsonify
from pydantic import ValidationError
from sqlalchemy import select
from api.v1.views.shared.auth.method import check_password, create_token
from api.v1.views.utils import student_teacher_or_admin_required
from api.v1.utils.typing import UserT
from api.v1.views.shared import auths as auth
from extension.pydantic.models.user_schema import UserSchema
from models import storage
from models.blacklist_token import BlacklistToken
from api.v1.views.shared.auth.schema import (
    AuthResponseSchema,
    AuthSchema,
    InvalidCredentialsError,
)
from api.v1.views import errors
from models.user import User


@auth.route("auth/login", methods=["POST"])
def login() -> Tuple[Response, int]:
    """
    Handle user login by validating credentials and generating an access token.
    """
    try:
        user_auth_schema = AuthSchema.model_validate(request.get_json())
        user = storage.session.scalar(
            select(User).where(
                User.identification == user_auth_schema.identification,
            )
        )
        if not user:
            raise InvalidCredentialsError("User not found.")

        # Validate the password
        if not check_password(user.password, user_auth_schema.password):
            raise InvalidCredentialsError("Invalid password.")

        user_schema = UserSchema.model_validate(user)

        # Generate an api_key token based on the user's role
        api_key = create_token(user_schema.id, user_schema.role)

        response = AuthResponseSchema(
            message="logged in successfully.",
            api_key=api_key,
            id=user_schema.id,
            role=user_schema.role,
        ).model_dump(by_alias=True)

        return jsonify(response), 200
    except ValidationError as e:
        return errors.handle_validation_error(error=e)
    except InvalidCredentialsError as e:
        return errors.handle_invalid_credentials_error(error=e)
    except Exception as e:
        return errors.handle_internal_error(error=e)


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
        return errors.handle_internal_error(error=e)
