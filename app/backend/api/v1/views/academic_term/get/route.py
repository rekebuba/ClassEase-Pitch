from typing import Tuple
import uuid
from flask import Response, jsonify
from sqlalchemy import select
from api.v1.utils.parameter import validate_expand, validate_fields
from api.v1.utils.typing import IncEx, UserT
from api.v1.views import base_api
from api.v1.views.utils import student_teacher_or_admin_required
from extension.pydantic.models.academic_term_schema import (
    AcademicTermRelationshipSchema,
    AcademicTermSchema,
    AcademicTermSchemaWithRelationships,
)
from extension.pydantic.response.schema import success_response
from models.academic_term import AcademicTerm
from models import storage


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
@validate_expand(AcademicTermRelationshipSchema)
def get_academic_term_by_id(
    user: UserT,
    fields: dict[str, IncEx],
    related_fields: dict[str, IncEx],
    term_id: uuid.UUID,
) -> Tuple[Response, int]:
    """
    Get a specific academic term by ID.
    """
    academic_term = storage.session.get(AcademicTerm, term_id)
    if not academic_term:
        return jsonify({"error": f"Academic term with ID {term_id} not found"}), 404

    term_schema = AcademicTermSchemaWithRelationships.model_validate(academic_term)
    valid_term = term_schema.model_dump(
        by_alias=True,
        include={
            **fields,
            **related_fields,
        },
        mode="json",
    )

    return success_response(data=valid_term)
