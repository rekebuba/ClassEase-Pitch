from typing import Set, Tuple
import uuid
from sqlalchemy import select
from api.v1.utils.parameter import validate_expand, validate_fields
from api.v1.utils.typing import IncEx, UserT
from api.v1.views import errors
from api.v1.views.shared import auths as auth
from api.v1.views.utils import student_teacher_or_admin_required
from extension.pydantic.models.grade_schema import GradeSchema
from extension.pydantic.models.subject_schema import (
    SubjectRelationshipSchema,
    SubjectSchema,
    SubjectWithRelationshipsSchema,
)
from extension.pydantic.response.schema import success_response
from models import storage
from models.grade import Grade
from models.subject import Subject
from flask import Response, jsonify

from models.yearly_subject import YearlySubject


@auth.route("/years/<uuid:year_id>/subjects", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(SubjectSchema, SubjectSchema.default_fields())
def get_available_subjects(
    user: UserT, fields: Set[str], year_id: uuid.UUID
) -> Tuple[Response, int]:
    """
    Returns a list of all available subjects in the system.
    """
    subjects = storage.session.scalars(
        select(Subject).where(Subject.year_id == year_id)
    ).all()

    subject_schemas = [SubjectSchema.model_validate(subject) for subject in subjects]
    valid_subjects = [
        schema.model_dump(by_alias=True, include=fields) for schema in subject_schemas
    ]
    return success_response(data=valid_subjects)


@auth.route("/subjects/<uuid:subject_id>", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(SubjectSchema, SubjectSchema.default_fields())
@validate_expand(SubjectRelationshipSchema)
def get_subject_by_id(
    user: UserT,
    fields: dict[str, IncEx],
    related_fields: dict[str, IncEx],
    subject_id: uuid.UUID,
) -> Tuple[Response, int]:
    """Returns Subject model based on subject_id"""
    subject = storage.session.get(Subject, subject_id)
    if not subject:
        return jsonify({"error": "Subject not found"}), 404

    subject_schema = SubjectWithRelationshipsSchema.model_validate(subject)
    valid_subject = subject_schema.model_dump(
        by_alias=True,
        include={
            **fields,
            **related_fields,
        },
        mode="json",
    )

    return success_response(data=valid_subject)
