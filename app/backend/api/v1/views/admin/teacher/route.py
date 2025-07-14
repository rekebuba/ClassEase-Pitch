import json
from typing import Tuple
from urllib.parse import parse_qs, urlparse

from extension.enums.enum import RoleEnum, StatusEnum
from extension.pydantic.models.teacher_schema import (
    TeacherSchema,
)
from flask import Response, jsonify, request, url_for
from api.v1.utils.typing import UserT
from api.v1.views.admin import admins as admin
from api.v1.views.utils import admin_required
from extension.pydantic.models.user_schema import UserSchema

from models.teacher import Teacher
from models.user import User
from models import storage
from api.v1.views import errors
from pydantic import TypeAdapter, ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from .schema import DetailApplicationResponse, UserCreateSchema


@admin.route("/teachers", methods=["GET"])
@admin_required
def all_teachers(admin_data: UserT) -> Tuple[Response, int]:
    """
    Retrieve and return a list of teachers with pagination and optional search functionality.

    Args:
        admin_data (dict): Data related to the admin making the request.
    """
    url = request.url
    parsed_url = urlparse(url)
    data = parse_qs(parsed_url.query)

    query = (
        storage.session.query(
            Teacher.id,
            Teacher.first_name.label("firstName"),
            Teacher.last_name.label("lastName"),
            Teacher.email,
            Teacher.no_of_mark_list.label("markList"),
            User.image_path,
        )
        .join(User, User.id == Teacher.id)
        .group_by(Teacher.id)
    )

    if not query:
        return jsonify({"message": "No teachers found"}), 404

    teacher_list = [
        {
            key: url_for("static", filename=value, _external=True)
            if key == "image_path" and value is not None
            else value
            for key, value in q._asdict().items()
        }
        for q in query
    ]

    return jsonify(
        {
            "teachers": teacher_list,
        }
    ), 200


@admin.route("/teacher/applications", methods=["GET"])
@admin_required
def teacher_applications(admin_data: UserT) -> Tuple[Response, int]:
    try:
        teachers = storage.session.query(Teacher).all()

        if not teachers:
            return jsonify({"message": "No teacher applications found"}), 404

        # Convert each SQLAlchemy model to a Pydantic schema
        adapter = TypeAdapter(list[TeacherSchema])
        teacher_schema_list = adapter.validate_python(teachers)
        teacher_schemas = [schema.model_dump() for schema in teacher_schema_list]

        return jsonify(teacher_schemas), 200
    except ValidationError as e:
        return errors.handle_validation_error(error=e)
    except SQLAlchemyError as e:
        storage.session.rollback()
        return errors.handle_database_error(error=e)
    except Exception as e:
        storage.session.rollback()
        return errors.handle_internal_error(error=e)


@admin.route("/teacher/applications/<string:id>", methods=["GET"])
@admin_required
def detail_teacher_application(admin_data: UserT, id: str) -> Tuple[Response, int]:
    """Retrieve detailed information about a specific teacher application by ID."""
    try:
        teacher = (
            storage.session.query(Teacher)
            .options(
                joinedload(Teacher.user),
                joinedload(Teacher.subjects_to_teach),
                joinedload(Teacher.grade_level),
            )
            .filter(Teacher.id == id)
            .first()
        )

        if not teacher:
            return jsonify({"message": "Teacher application not found"}), 404

        # Convert the SQLAlchemy model to a Pydantic schema
        teacher_schema = DetailApplicationResponse.model_validate(
            {
                "subjects_to_teach": [
                    subject.name for subject in teacher.subjects_to_teach
                ],
                "grade_levels_to_teach": [grade.grade for grade in teacher.grade_level],
            }
        )

        return jsonify(teacher_schema.model_dump(by_alias=True)), 200
    except ValidationError as e:
        return errors.handle_validation_error(error=e)
    except SQLAlchemyError as e:
        storage.session.rollback()
        return errors.handle_database_error(error=e)
    except Exception as e:
        storage.session.rollback()
        return errors.handle_internal_error(error=e)


@admin.route("/teacher/applications/<string:id>", methods=["PUT"])
@admin_required
def update_teacher_application_status(
    admin_data: UserT, id: str
) -> Tuple[Response, int]:
    """Update the status of a teacher application."""
    try:
        data = request.get_json()
        if not data or "status" not in data:
            return jsonify({"message": "Invalid request data"}), 400

        status = data["status"]
        if status not in StatusEnum._value2member_map_:
            return jsonify({"message": "Invalid status"}), 400

        status_enum = StatusEnum(status)

        teacher = storage.session.query(Teacher).filter(Teacher.id == id).first()
        if not teacher:
            return jsonify({"message": "Teacher application not found"}), 404

        teacher.status = status_enum

        if status_enum == StatusEnum.APPROVED and teacher.user is None:
            # If accepted, set the teacher's user
            user_data = UserCreateSchema.model_validate(
                {
                    "role": RoleEnum.TEACHER,
                    "national_id": teacher.social_security_number,
                }
            )
            if user_data.identification is None or user_data.password is None:
                raise ValueError(
                    "Failed to generate identification and password for teacher"
                )
            teacher.user = User(
                identification=user_data.identification,
                password=user_data.password,
                role=user_data.role,
                national_id=user_data.national_id,
            )

        storage.session.commit()

        return jsonify(
            {"message": "Teacher application status updated successfully"}
        ), 200
    except ValidationError as e:
        return errors.handle_validation_error(error=e)
    except SQLAlchemyError as e:
        storage.session.rollback()
        return errors.handle_database_error(error=e)
    except Exception as e:
        storage.session.rollback()
        return errors.handle_internal_error(error=e)
    except ValueError as e:
        storage.session.rollback()
        return errors.handle_internal_error(error=e)
