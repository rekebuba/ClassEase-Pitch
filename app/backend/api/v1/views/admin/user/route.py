from typing import Callable, Dict, Tuple
from sqlalchemy.exc import SQLAlchemyError
from flask import Response, jsonify, request
from api.v1.utils.typing import UserT
from api.v1.views import errors
from api.v1.views.admin import admins as admin
from api.v1.views.admin.user.method import generate_id, hash_password
from api.v1.views.admin.user.schema import NewUserSchema, SucssussfulLinkResponse
from api.v1.views.utils import admin_required
from extension.enums.enum import RoleEnum
from extension.pydantic.models.user_schema import UserSchema
from models import storage
from models.admin import Admin
from models.student import Student
from models.teacher import Teacher
from models.user import User
from models.year import Year


@admin.route("/user/<user_id>", methods=["GET"])
@admin_required
def get_user_by_id(admin_data: UserT, user_id: str) -> Tuple[Response, int]:
    """
    Retrieve user details by user ID.
    """
    try:
        user = storage.session.query(User).filter_by(id=user_id).one_or_none()
        if not user:
            return jsonify({"message": "User not found"}), 404

        user_schema = UserSchema.model_validate(user)
        return jsonify(user_schema.model_dump()), 200
    except SQLAlchemyError as e:
        return errors.handle_database_error(e)


@admin.route("/link_user/<id>", methods=["POST"])
@admin_required
def link_to_user(admin_data: UserT, id: str) -> Tuple[Response, int]:
    """
    Link a user to an admin or Student or Teacher.
    """
    try:
        # fetch the data from query parameter
        data = NewUserSchema.model_validate(request.get_json())
        if not data:
            return jsonify({"message": "No data provided"}), 400

        academic_year = storage.session.get(Year, data.academic_id)
        if not academic_year:
            return jsonify({"message": "Academic year not found"}), 404

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

        if not data.identification:
            data.identification = generate_id(data.role, academic_year.ethiopian_year)

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

        response = SucssussfulLinkResponse(
            message="User linked successfully",
            id=new_user.id,
        )

        return jsonify(response.model_dump(by_alias=True)), 201
    except SQLAlchemyError as e:
        storage.session.rollback()
        return errors.handle_database_error(e)
    except Exception as e:
        storage.session.rollback()
        return errors.handle_internal_error(e)
