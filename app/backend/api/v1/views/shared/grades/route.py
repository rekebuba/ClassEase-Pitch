from typing import Set, Tuple
import uuid
from sqlalchemy import select
from api.v1.utils.parameter import validate_fields
from api.v1.utils.typing import UserT
from api.v1.views.shared import auths as auth
from api.v1.views.utils import student_teacher_or_admin_required
from extension.pydantic.models.grade_schema import GradeSchema
from extension.pydantic.response.schema import success_response
from models import storage
from models.grade import Grade
from flask import Response, jsonify

@auth.route("/years/<uuid:year_id>/grades", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(GradeSchema, GradeSchema.default_fields())
def grades(user: UserT, fields: Set[str], year_id: uuid.UUID) -> Tuple[Response, int]:
    """
    Returns a list of all available grades in the system.
    """
    grades = storage.session.scalars(
        select(Grade).where(Grade.year_id == year_id)
    ).all()

    grade_schemas = [GradeSchema.model_validate(grade) for grade in grades]
    valid_grades = [
        schema.model_dump(by_alias=True, include=fields) for schema in grade_schemas
    ]

    print(valid_grades)

    return success_response(data=valid_grades)


@auth.route("/grades/<uuid:grade_id>", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(GradeSchema, GradeSchema.default_fields())
def get_grade_by_id(
    user: UserT,
    fields: Set[str],
    grade_id: uuid.UUID,
) -> Tuple[Response, int]:
    """Returns Grade model based on grade_id"""
    grade = storage.session.scalar(select(Grade).where(Grade.id == grade_id))
    if not grade:
        return jsonify({"error": "Grade not found"}), 404

    grade_schema = GradeSchema.model_validate(grade)
    valid_grade = grade_schema.model_dump(by_alias=True, include=fields)

    return success_response(data=valid_grade)
