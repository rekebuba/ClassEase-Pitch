from typing import Tuple
import uuid
from flask import Response, jsonify
from sqlalchemy import select
from api.v1.utils.parameter import validate_expand, validate_fields
from api.v1.utils.typing import IncEx, UserT
from api.v1.views.utils import student_teacher_or_admin_required
from extension.pydantic.models.teacher_schema import (
    TeacherRelatedSchema,
    TeacherSchema,
    TeacherWithRelatedSchema,
)
from extension.pydantic.response.schema import success_response
from models.teacher import Teacher
from models import storage
from models.teacher_year_link import TeacherYearLink
from api.v1.views import base_api

@base_api.route("/years/<uuid:year_id>/teachers", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(TeacherSchema, TeacherSchema.default_fields())
def get_teacher_info(
    user: UserT,
    fields: set[str],
    year_id: uuid.UUID,
) -> Tuple[Response, int]:
    """Get all teachers' information."""
    teachers = (
        storage.session.execute(
            select(Teacher)
            .join(TeacherYearLink, Teacher.id == TeacherYearLink.teacher_id)
            .where(TeacherYearLink.year_id == year_id)
        )
        .scalars()
        .all()
    )

    if not teachers:
        return jsonify({"error": "No teachers found"}), 404

    teacher_schema = [TeacherSchema.model_validate(teacher) for teacher in teachers]
    response = [
        teacher.model_dump(
            by_alias=True,
            exclude_none=True,
            include=fields,
            mode="json",
        )
        for teacher in teacher_schema
    ]

    return success_response(data=response)


@base_api.route("/teachers/<uuid:teacher_id>", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(TeacherSchema, TeacherSchema.default_fields())
@validate_expand(TeacherRelatedSchema)
def get_teacher_by_id(
    user: UserT,
    fields: dict[str, IncEx],
    related_fields: dict[str, IncEx],
    teacher_id: uuid.UUID,
) -> Tuple[Response, int]:
    """
    Get a specific teacher by ID.

    Args:
        user (UserT): The user object containing teacher identifiers.
        fields (set[str]): Fields to include in the response.
        teacher_id (uuid.UUID): The ID of the teacher to retrieve.

    Returns:
        Tuple[Response, int]: JSON response with teacher information and status code.
    """
    teacher = storage.session.scalar(select(Teacher).where(Teacher.id == teacher_id))

    if not teacher:
        return jsonify({"error": f"Teacher with the id {teacher_id} not found"}), 404

    teacher_schema = TeacherWithRelatedSchema.model_validate(teacher)
    response = teacher_schema.model_dump(
        by_alias=True,
        exclude_none=True,
        include={**fields, **related_fields},
        mode="json",
    )

    return success_response(data=response)
