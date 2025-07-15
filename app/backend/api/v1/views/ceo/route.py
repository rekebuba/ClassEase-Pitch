from typing import Callable, Dict, Tuple
from sqlalchemy.exc import SQLAlchemyError
from flask import Response, jsonify, request
from api.v1.views import errors
from api.v1.views.ceo.schema import NewAdminSchema
from api.v1.views.shared import auths as auth
from api.v1.views.admin.user.method import generate_id, hash_password
from api.v1.views.utils import ceo_required
from extension.enums.enum import RoleEnum
from extension.functions.helper import current_EC_year
from extension.pydantic.models.user_schema import UserSchema
from extension.pydantic.response.schema import success_response
from models import storage
from models.admin import Admin
from models.ceo import CEO
from models.student import Student
from models.teacher import Teacher
from models.user import User


@auth.route("/ceo/approve/<string:id>", methods=["POST"])
@ceo_required
def link_to_user(CEO_data: CEO, id: str) -> Tuple[Response, int]:
    """
    Link a user to an admin or Student or Teacher.
    """
    try:
        # fetch the data from query parameter
        data = NewAdminSchema.model_validate(request.get_json())
        if not data:
            return jsonify({"message": "No data provided"}), 400

        role_lookup: Dict[str, Callable[[], Admin | Student | Teacher | None]] = {
            RoleEnum.ADMIN.value: lambda: storage.session.get(Admin, id),
            RoleEnum.STUDENT.value: lambda: storage.session.get(Student, id),
            RoleEnum.TEACHER.value: lambda: storage.session.get(Teacher, id),
        }

        getter = role_lookup.get(data.role)
        if getter is None:
            return jsonify({"message": "Invalid role provided"}), 400

        valid_role = getter()
        if not valid_role:
            return jsonify({"message": "Invalid role ID provided"}), 400

        if valid_role.user_id:
            return jsonify({"message": "This role is already linked to a user"}), 400

        if not data.identification:
            data.identification = generate_id(data.role, current_EC_year())

        if not data.password:
            # TODO: Implement a secure password generation method
            data.password = hash_password(data.identification)

        new_user = User(
            identification=data.identification,
            password=data.password,
            role=data.role,
        )
        valid_role.user_id = new_user.id

        storage.session.add(new_user)
        storage.session.commit()

        user_schema = UserSchema.model_validate(new_user)
        new_user_schema = user_schema.model_dump(
            by_alias=True,
            exclude_none=True,
            mode="json",
        )

        return success_response(
            message="User linked successfully", data=new_user_schema
        )
    except SQLAlchemyError as e:
        storage.session.rollback()
        return errors.handle_database_error(error=e)
    except Exception as e:
        storage.session.rollback()
        return errors.handle_internal_error(error=e)
