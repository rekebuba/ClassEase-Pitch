from typing import Tuple
import uuid
from flask import Response, jsonify
from sqlalchemy import select
from api.v1.utils.parameter import validate_fields
from api.v1.utils.typing import IncEx, UserT
from api.v1.views import base_api
from api.v1.views.utils import student_teacher_or_admin_required
from extension.pydantic.models.academic_term_schema import AcademicTermSchema
from extension.pydantic.models.year_schema import (
    YearRelationshipSchema,
    YearSchema,
    YearSchemaWithRelationships,
)
from extension.pydantic.response.schema import success_response
from models.academic_term import AcademicTerm
from models import storage
from models.student import Student


@base_api.route("/years/<uuid:year_id>/academic_terms", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(AcademicTermSchema, AcademicTermSchema.default_fields())
def get_academic_terms(
    user: UserT,
    fields: set[str],
    year_id: uuid.UUID,
) -> Tuple[Response, int]:
    """
    Get all academic terms.
    """
    academic_terms = storage.session.scalars(
        select(AcademicTerm).where(AcademicTerm.year_id == year_id)
    ).all()

    if not academic_terms:
        return jsonify({"error": "No academic terms found"}), 404

    academic_term_schemas = [
        AcademicTermSchema.model_validate(term) for term in academic_terms
    ]
    response = [
        term.model_dump(
            by_alias=True,
            include=fields,
            mode="json",
        )
        for term in academic_term_schemas
    ]

    return success_response(data=response)


@base_api.route("/academic_terms/<uuid:term_id>", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(AcademicTermSchema, AcademicTermSchema.default_fields())
def get_academic_term_by_id(
    user: UserT,
    fields: set[str],
    term_id: uuid.UUID,
) -> Tuple[Response, int]:
    """
    Get a specific academic term by ID.
    """
    academic_term = storage.session.get(AcademicTerm, term_id)
    if not academic_term:
        return jsonify({"error": f"Academic term with ID {term_id} not found"}), 404

    term_schema = AcademicTermSchema.model_validate(academic_term)
    valid_term = term_schema.model_dump(by_alias=True, include=fields, mode="json")

    return success_response(data=valid_term)


@base_api.route("/students/<uuid:student_id>/years/academic_terms", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(YearSchema, YearSchema.default_fields(), "year_fields")
@validate_fields(AcademicTermSchema, AcademicTermSchema.default_fields(), "academic_term_fields")
def get_academic_terms_for_student(
    user: UserT,
    year_fields: dict[str, IncEx],
    academic_term_fields: dict[str, IncEx],
    student_id: uuid.UUID,
) -> Tuple[Response, int]:
    """
    Get all academic terms associated with a specific student.
    """
    student = storage.session.scalar(select(Student).where(Student.id == student_id))

    if not student:
        return jsonify({"error": f"No student found with ID {student_id}"}), 404

    # Define your field filters
    merged_fields: IncEx = {
        **year_fields,
        "academic_terms": {
            "__all__": academic_term_fields
        },  # Include these fields for all terms
    }

    response = [
        YearSchemaWithRelationships.model_validate(year).model_dump(
            by_alias=True, include=merged_fields, mode="json"
        )
        for year in student.year_links
    ]

    return success_response(data=response)
