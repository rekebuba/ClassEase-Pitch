#!/usr/bin/python3
"""Public views module for the API"""

from flask import Response, request, jsonify
from marshmallow import ValidationError
from typing import Tuple
from api.v1.views.shared import auths as auth
from api.v1.views.methods import parse_nested_form
from api.v1.views.shared.registration.methods import create_role_based_user
from api.v1.views.shared.registration.schema import DumpResultSchema
from models.base_model import CustomTypes
from models import storage
from api.v1.views import errors


@auth.route("/registration/<role>", methods=["POST"])
def register_new_user(role: str) -> Tuple[Response, int]:
    """
    Registers a new user (Admin, Student, Teacher) in the system.
    """

    try:
        data_to_parse = {**request.form.to_dict(), **request.files.to_dict()}
        data = parse_nested_form(data_to_parse)
        role_enum = CustomTypes.RoleEnum.enum_value(role.lower())

        if not data:
            raise Exception("No data provided")

        result = create_role_based_user(role_enum, data)
        if not result:
            raise Exception("Failed to register user")

        validate_data = {
            "message": f"{role} registered successfully!",
            "user": {
                "identification": result.identification,
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
