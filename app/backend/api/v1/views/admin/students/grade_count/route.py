from typing import Tuple

from flask import Response, jsonify
from sqlalchemy import func
from api.v1.utils.typing import UserT
from api.v1.views.admin import admins as admin
from api.v1.views.admin.students.grade_count.schema import (
    StudentGradeCountsSchema,
)
from api.v1.views.utils import admin_required
from models.grade import Grade
from models.stud_year_record import STUDYearRecord

from models import storage


@admin.route("/students/grade-counts", methods=["GET"])
@admin_required
def student_grade_counts(admin_data: UserT) -> Tuple[Response, int]:
    """
    Retrieve and return the count of students in each grade.

    Returns:
        Response: A JSON response containing the count of students in each grade.
                  If no students are found, returns a 404 error with an appropriate message.
    """
    query = (
        storage.session.query(
            Grade.grade, func.count(STUDYearRecord.grade_id).label("grade_count")
        )
        .join(STUDYearRecord.grades)
        .group_by(Grade.id)
        .order_by(Grade.grade)
    )
    # Process results
    result = query.all()

    data_to_serialize = [
        {"grade": grade, "total": grade_count} for grade, grade_count in result
    ]

    # Return the serialized data
    schema = StudentGradeCountsSchema(many=True)
    result = schema.dump(data_to_serialize)

    return jsonify(result), 200
