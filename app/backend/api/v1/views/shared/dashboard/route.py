from typing import Tuple
import uuid
from flask import Response
from sqlalchemy import select
from extension.pydantic.models.student_schema import (
    StudentRelationshipSchema,
    StudentSchema,
    StudentWithRelationshipsSchema,
)
from extension.pydantic.models.teacher_schema import (
    TeacherRelationshipSchema,
    TeacherSchema,
    TeacherWithRelationshipsSchema,
)
from extension.pydantic.response.schema import error_response, success_response
from models import storage
from api.v1.utils.parameter import validate_expand, validate_fields
from api.v1.utils.typing import IncEx, UserT
from api.v1.views.shared import auths as auth
from api.v1.views.utils import (
    student_teacher_or_admin_required,
    admin_required,
    student_required,
    teacher_required,
)
from extension.pydantic.models.admin_schema import (
    AdminRelationshipSchema,
    AdminSchema,
    AdminWithRelationshipsSchema,
)
from extension.pydantic.models.user_schema import UserSchema
from models.admin import Admin
from models.student import Student
from models.teacher import Teacher


@auth.route("/users/<uuid:user_id>", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(UserSchema, UserSchema.default_fields())
def user(
    user: UserT,
    fields: dict[str, IncEx],
    user_id: uuid.UUID,
) -> Tuple[Response, int]:
    if user_id != user.id:
        return error_response(message=f"invalid User ID {user_id} Provided.")

    user_schema = UserSchema.model_validate(user)
    response = user_schema.model_dump(by_alias=True, include=fields, mode="json")

    return success_response(data=response)


@auth.route("/users/<uuid:user_id>/admin", methods=["GET"])
@admin_required
@validate_fields(AdminSchema, AdminSchema.default_fields())
@validate_expand(AdminRelationshipSchema)
def admin_data(
    user: UserT,
    fields: dict[str, IncEx],
    related_fields: dict[str, IncEx],
    user_id: uuid.UUID,
) -> Tuple[Response, int]:
    """"""
    admin = storage.session.scalar(select(Admin).where(Admin.user_id == user_id))
    if not admin:
        return error_response(message=f"User with ID {user_id} not found.", status=404)

    admin_schema = AdminWithRelationshipsSchema.model_validate(admin)
    response = admin_schema.model_dump(
        by_alias=True,
        include={
            **fields,
            **related_fields,
        },
        mode="json",
    )

    return success_response(data=response)


@auth.route("/users/<uuid:user_id>/student", methods=["GET"])
@student_required
@validate_fields(StudentSchema, StudentSchema.default_fields())
@validate_expand(StudentRelationshipSchema)
def student_data(
    user: UserT,
    fields: dict[str, IncEx],
    related_fields: dict[str, IncEx],
    user_id: uuid.UUID,
) -> Tuple[Response, int]:
    """"""
    student = storage.session.scalar(select(Student).where(Student.user_id == user_id))
    if not student:
        return error_response(message=f"User with ID {user_id} not found.", status=404)

    student_schema = StudentWithRelationshipsSchema.model_validate(student)
    response = student_schema.model_dump(
        by_alias=True,
        include={
            **fields,
            **related_fields,
        },
        mode="json",
    )

    return success_response(data=response)


@auth.route("/users/<uuid:user_id>/teacher", methods=["GET"])
@teacher_required
@validate_fields(TeacherSchema, TeacherSchema.default_fields())
@validate_expand(TeacherRelationshipSchema)
def teacher_data(
    user: UserT,
    fields: dict[str, IncEx],
    related_fields: dict[str, IncEx],
    user_id: uuid.UUID,
) -> Tuple[Response, int]:
    """"""
    teacher = storage.session.scalar(select(Teacher).where(Teacher.user_id == user_id))
    if not teacher:
        return error_response(message=f"User with ID {user_id} not found.", status=404)

    teacher_schema = TeacherWithRelationshipsSchema.model_validate(teacher)
    response = teacher_schema.model_dump(
        by_alias=True,
        include={
            **fields,
            **related_fields,
        },
        mode="json",
    )

    return success_response(data=response)
