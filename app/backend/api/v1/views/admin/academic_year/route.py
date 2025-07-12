from typing import Tuple
from flask import Response, jsonify
from sqlalchemy import select
from api.v1.utils.typing import UserT
from api.v1.views.admin import admins as admin
from api.v1.views.utils import admin_required
from extension.pydantic.models.section_schema import SectionSchema
from models.grade import Grade
from models import storage
from models.year import Year


@admin.route(
    "/academic_year/<string:year_id>/grade/<string:grade_id>/section", methods=["GET"]
)
@admin_required
def get_section_for_grade(
    user: UserT, year_id: str, grade_id: str
) -> Tuple[Response, int]:
    """Get a specific academic year grade by ID."""
    grade = storage.session.scalar(
        select(Grade)
        .join(Year, Year.id == Grade.year_id)
        .where(Grade.id == grade_id, Year.id == year_id)
    )
    if not grade:
        return jsonify({"error": "Grade not found"}), 404

    section_schemas = [
        SectionSchema.model_validate(section) for section in grade.sections_link
    ]
    return jsonify(
        [section.model_dump(by_alias=True, mode="json") for section in section_schemas]
    ), 200
