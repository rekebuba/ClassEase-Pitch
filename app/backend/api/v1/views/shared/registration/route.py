#!/usr/bin/python3
"""Public views module for the API"""

from flask import Response, request, jsonify
from marshmallow import ValidationError
from typing import Tuple
from api.v1.views.shared import auths as auth
from api.v1.views.methods import create_role_based_user
from api.v1.views.shared.registration.schema import DumpResultSchema
from models.base_model import CustomTypes
from models import storage
from api.v1.views import errors


@auth.route("/registration/<role>", methods=["POST"])
def register_new_user(role: str) -> Tuple[Response, int]:
    """
    Registers a new user (Admin, Student, Teacher) in the system.

    Args:
        role (str): The role of the user to be registered. It should be one of 'Admin', 'Student', or 'Teacher'.

    Returns:
        Response: A JSON response indicating the success or failure of the registration process.
    """

    try:
        role_enum = CustomTypes.RoleEnum.enum_value(role.lower())

        data = {
            **request.form.to_dict(),
            "role": role_enum,
            "image_path": request.files.get("image_path"),
        }

        if not data:
            raise Exception("No data provided")

        result = create_role_based_user(role_enum, data)
        if not result:
            raise Exception("Failed to register user")

        validate_data = {
            "message": f"{role} registered successfully!",
            "user": {
                "id": result.identification,
                "role": result.role,
            },
        }

        schema = DumpResultSchema()
        send_result = schema.dump(validate_data)

        return jsonify(**send_result), 201
    except ValidationError as e:
        storage.rollback()
        return errors.handle_validation_error(e)
    except Exception as e:
        storage.rollback()
        return errors.handle_internal_error(e)
