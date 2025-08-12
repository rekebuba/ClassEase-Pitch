from typing import Tuple
import uuid
from flask import Response, jsonify
from sqlalchemy import select
from api.v1.utils.parameter import validate_expand, validate_fields
from api.v1.utils.typing import IncEx, UserT
from api.v1.views.utils import student_teacher_or_admin_required
from api.v1.views.student import stud
from extension.pydantic.models.student_schema import (
    StudentRelatedSchema,
    StudentSchema,
    StudentWithRelatedSchema,
)
from extension.pydantic.response.schema import success_response
from models.student import Student
from models import storage
from models.student_year_link import StudentYearLink


@stud.route("/years/<uuid:year_id>/students", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(StudentSchema, StudentSchema.default_fields())
def get_student_info(
    user: UserT,
    fields: set[str],
    year_id: uuid.UUID,
) -> Tuple[Response, int]:
    """Get all students' information."""
    students = (
        storage.session.execute(
            select(Student)
            .join(StudentYearLink, Student.id == StudentYearLink.student_id)
            .where(StudentYearLink.year_id == year_id)
        )
        .scalars()
        .all()
    )

    if not students:
        return jsonify({"error": "No students found"}), 404

    student_schema = [StudentSchema.model_validate(student) for student in students]
    response = [
        student.model_dump(
            by_alias=True,
            exclude_none=True,
            include=fields,
            mode="json",
        )
        for student in student_schema
    ]

    return success_response(data=response)


@stud.route("/students/<uuid:student_id>", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(StudentSchema, StudentSchema.default_fields())
@validate_expand(StudentRelatedSchema)
def get_student_by_id(
    user: UserT,
    fields: dict[str, IncEx],
    related_fields: dict[str, IncEx],
    student_id: uuid.UUID,
) -> Tuple[Response, int]:
    """
    Get a specific student by ID.

    Args:
        user (UserT): The user object containing student identifiers.
        fields (set[str]): Fields to include in the response.
        student_id (uuid.UUID): The ID of the student to retrieve.

    Returns:
        Tuple[Response, int]: JSON response with student information and status code.
    """
    student = storage.session.scalar(select(Student).where(Student.id == student_id))

    if not student:
        return jsonify({"error": f"Student with the id {student_id} not found"}), 404

    student_schema = StudentWithRelatedSchema.model_validate(student)
    response = student_schema.model_dump(
        by_alias=True,
        exclude_none=True,
        include={**fields, **related_fields},
        mode="json",
    )

    return success_response(data=response)
