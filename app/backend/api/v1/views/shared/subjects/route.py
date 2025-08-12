from typing import Any, Dict, Tuple
import uuid
from sqlalchemy import select
from api.v1.utils.test_parameter import query_parameters
from api.v1.utils.typing import UserT
from api.v1.views.shared import auths as auth
from api.v1.views.utils import student_teacher_or_admin_required
from extension.pydantic.models.subject_schema import SubjectNestedSchema
from extension.pydantic.response.schema import error_response, success_response
from models import storage
from models.subject import Subject
from flask import Response, jsonify

from models.year import Year


@auth.route("/years/<uuid:year_id>/subjects", methods=["GET"])
@student_teacher_or_admin_required
@query_parameters(SubjectNestedSchema)
def get_available_subjects(
    user: UserT,
    include_params: Dict[str, Any],
    year_id: uuid.UUID,
) -> Tuple[Response, int]:
    """
    Returns a list of all available subjects in the system.
    """
    if not storage.session.get(Year, year_id):
        return error_response(message=f"Year with ID {year_id} not found.", status=404)

    subjects = storage.session.scalars(
        select(Subject).where(Subject.year_id == year_id)
    ).all()

    subject_schemas = [
        SubjectNestedSchema.model_validate(subject).model_dump(
            by_alias=True,
            include=include_params,
            mode="json",
        )
        for subject in subjects
    ]

    return success_response(data=subject_schemas)


@auth.route("/subjects/<uuid:subject_id>", methods=["GET"])
@student_teacher_or_admin_required
@query_parameters(SubjectNestedSchema)
def get_subject_by_id(
    user: UserT,
    include_params: Dict[str, Any],
    subject_id: uuid.UUID,
) -> Tuple[Response, int]:
    """Returns Subject model based on subject_id"""
    subject = storage.session.get(Subject, subject_id)
    if not subject:
        return jsonify({"error": "Subject not found"}), 404

    subject_schema = SubjectNestedSchema.model_validate(subject)
    valid_subject = subject_schema.model_dump(
        by_alias=True,
        include=include_params,
        mode="json",
    )

    return success_response(data=valid_subject)


@auth.route("/tests/subjects/<uuid:subject_id>", methods=["GET"])
@student_teacher_or_admin_required
@query_parameters(SubjectNestedSchema)
def get_subject_by_id_test(
    user: UserT,
    include_params: dict[str, Any],
    subject_id: uuid.UUID,
) -> Tuple[Response, int]:
    """Returns Subject model based on subject_id"""
    subject = storage.session.get(Subject, subject_id)
    if not subject:
        return jsonify({"error": "Subject not found"}), 404

    subject_schema = SubjectNestedSchema.model_validate(subject)
    valid_subject = subject_schema.model_dump(
        by_alias=True,
        include=include_params,
        mode="json",
    )

    return success_response(data=valid_subject)
