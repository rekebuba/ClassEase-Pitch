from typing import Set, Tuple
import uuid
from flask import Response, jsonify
from sqlalchemy import select
from api.v1.utils.parameter import validate_fields
from api.v1.utils.typing import UserT
from api.v1.views.shared import auths as auth
from api.v1.views.utils import student_teacher_or_admin_required
from extension.pydantic.models.section_schema import SectionSchema
from extension.pydantic.response.schema import success_response
from models import storage
from models.grade import Grade
from models.section import Section
from models.student_term_record import StudentTermRecord


@auth.route("/years/<uuid:year_id>/sections", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(SectionSchema, SectionSchema.default_fields())
def get_sections(
    user: UserT,
    fields: Set[str],
    year_id: uuid.UUID,
) -> Tuple[Response, int]:
    """
    Get all sections.

    Returns:
        Tuple[Response, int]: JSON response with sections and status code.
    """
    sections = storage.session.scalars(
        select(Section).where(Section.year_id == year_id)
    ).all()

    sections_schema = [SectionSchema.model_validate(section) for section in sections]
    response = [
        section_schema.model_dump(
            by_alias=True,
            exclude_none=True,
            include=fields,
            mode="json",
        )
        for section_schema in sections_schema
    ]

    return success_response(data=response)


@auth.route("student_term/<uuid:student_term_id>/sections", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(SectionSchema, SectionSchema.default_fields())
def get_section_for_student_term(
    user: UserT,
    fields: Set[str],
    student_term_id: uuid.UUID,
) -> Tuple[Response, int]:
    """Get a specific academic year grade by ID."""
    student_term = storage.session.scalar(
        select(StudentTermRecord).where(StudentTermRecord.id == student_term_id)
    )
    if not student_term:
        return jsonify({"error": "Student Term Record not found"}), 404

    section_schemas = SectionSchema.model_validate(student_term.section)
    result = section_schemas.model_dump(by_alias=True, mode="json", include=fields)

    return success_response(data=result, message="Sections retrieved successfully")


@auth.route("grades/<uuid:grade_id>/sections", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(SectionSchema, SectionSchema.default_fields())
def get_section_for_grade(
    user: UserT,
    fields: Set[str],
    grade_id: uuid.UUID,
) -> Tuple[Response, int]:
    """Get a specific academic year grade by ID."""
    grade = storage.session.scalar(select(Grade).where(Grade.id == grade_id))
    if not grade:
        return jsonify({"error": "Grade not found"}), 404

    section_schemas = [
        SectionSchema.model_validate(section) for section in grade.sections_link
    ]
    result = [
        section.model_dump(by_alias=True, mode="json", include=fields)
        for section in section_schemas
    ]

    return success_response(data=result, message="Sections retrieved successfully")


@auth.route("/sections/<uuid:section_id>", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(SectionSchema, SectionSchema.default_fields())
def get_section_by_id(
    user: UserT,
    fields: Set[str],
    section_id: uuid.UUID,
) -> Tuple[Response, int]:
    """
    Get a section by its ID.

    Args:
        section_id (str): The ID of the section.

    """
    section = storage.session.scalar(select(Section).where(Section.id == section_id))
    if not section:
        return jsonify({"error": "Section not found"}), 404

    section_schema = SectionSchema.model_validate(section)
    section_response = section_schema.model_dump(
        by_alias=True,
        exclude_none=True,
        include=fields,
        mode="json",
    )

    return success_response(data=section_response)
