from typing import Any, Dict, Tuple
import uuid
from sqlalchemy import select
from api.v1.utils.test_parameter import query_parameters
from api.v1.utils.typing import UserT
from api.v1.views.shared import auths as auth
from api.v1.views.utils import student_teacher_or_admin_required
from extension.pydantic.models.grade_schema import GradeNestedSchema
from extension.pydantic.response.schema import error_response, success_response
from models import storage
from models.grade import Grade
from models.year import Year
from flask import Response, jsonify


@auth.route("/years/<uuid:year_id>/grades", methods=["GET"])
@student_teacher_or_admin_required
@query_parameters(GradeNestedSchema)
def grades(
    user: UserT,
    include_params: Dict[str, Any],
    year_id: uuid.UUID,
) -> Tuple[Response, int]:
    """
    Returns a list of all available grades in the system.
    """
    if not storage.session.get(Year, year_id):
        return error_response(message=f"Year with ID {year_id} not found.", status=404)

    grades = storage.session.scalars(
        select(Grade).where(Grade.year_id == year_id)
    ).all()

    grade_schemas = [
        GradeNestedSchema.model_validate(grade).model_dump(
            by_alias=True,
            include=include_params,
            mode="json",
        )
        for grade in grades
    ]

    return success_response(data=grade_schemas)


@auth.route("/grades/<uuid:grade_id>", methods=["GET"])
@student_teacher_or_admin_required
@query_parameters(GradeNestedSchema)
def get_grade_by_id(
    user: UserT,
    include_params: Dict[str, Any],
    grade_id: uuid.UUID,
) -> Tuple[Response, int]:
    """Returns Grade model based on grade_id"""
    grade = storage.session.scalar(select(Grade).where(Grade.id == grade_id))
    if not grade:
        return jsonify({"error": "Grade not found"}), 404

    grade_schema = GradeNestedSchema.model_validate(grade)
    valid_grade = grade_schema.model_dump(
        by_alias=True,
        include=include_params,
        mode="json",
    )

    return success_response(data=valid_grade)
