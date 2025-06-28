# Define a type alias for the query result
from typing import Callable, Dict, Optional, Union, Tuple

from flask import Response, jsonify
from marshmallow import ValidationError
from sqlalchemy import Row
from api.v1.utils.typing import UserT
from api.v1.views import errors
from api.v1.views.shared import auths as auth
from api.v1.views.shared.dashboard.schema import UserDetailSchema
from api.v1.views.utils import student_teacher_or_admin_required
from extension.enums.enum import RoleEnum
from models.admin import Admin

from models.student import Student
from models.teacher import Teacher
from models.user import User
from models import storage

QueryResult = Optional[
    Union[Row[Tuple[User, Admin]], Row[Tuple[User, Teacher]], Row[Tuple[User, Student]]]
]

# Define the query dictionary type
QueryDict = Dict[RoleEnum, Callable[[], QueryResult]]


@auth.route("/", methods=["GET"])
@student_teacher_or_admin_required
def user(user: UserT) -> Tuple[Response, int]:
    query: QueryDict = {
        RoleEnum.ADMIN: lambda: (
            storage.session.query(User, Admin)
            .join(User.admins)
            .filter(User.id == user.id)
            .first()
        ),
        RoleEnum.TEACHER: lambda: (
            storage.session.query(User, Teacher)
            .join(User.teachers)
            .filter(User.id == user.id)
            .first()
        ),
        RoleEnum.STUDENT: lambda: (
            storage.session.query(User, Student)
            .join(User.students)
            .filter(User.id == user.id)
            .first()
        ),
    }
    try:
        if not query:
            return errors.handle_not_found_error("User Not Found")

        user_query = query[user.role]()
        if user_query is None:
            return errors.handle_not_found_error("User Not Found")

        user_data, detail = user_query
        # Serialize the data using the schema
        schema = UserDetailSchema()
        result = schema.dump({"user": user_data, "detail": detail})

        return jsonify(result), 200

    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)
