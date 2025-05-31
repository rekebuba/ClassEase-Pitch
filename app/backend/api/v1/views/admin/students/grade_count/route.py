from typing import Dict, Tuple

from flask import Response, jsonify
from marshmallow import ValidationError
from sqlalchemy import func
from api.v1.utils.typing import UserT
from api.v1.views import errors
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
    try:
        query = (
            storage.session.query(
                Grade.grade, func.count(STUDYearRecord.grade_id).label("grade_count")
            )
            .join(STUDYearRecord.grades)
            .group_by(Grade.id)
            .order_by(Grade.grade)
        ).all()

        # Process results
        serialize: Dict[str, int] = {str(i): 0 for i in range(1, 13)}
        for grade, grade_count in query:
            if grade is not None:
                serialize[str(grade)] = grade_count

        # Return the serialized data
        schema = StudentGradeCountsSchema()
        result = schema.dump({"data": serialize})

        return jsonify(**result["data"]), 200
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)
