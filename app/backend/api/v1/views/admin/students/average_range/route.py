from typing import Tuple

from flask import Response, jsonify
from marshmallow import ValidationError
from api.v1.utils.typing import UserT
from api.v1.views.admin import admins as admin
from api.v1.views.utils import admin_required

from api.v1.views.admin.students.average_range.schema import (
    StudentAverageSchema,
)
from api.v1.views.methods import (
    min_max_semester_lookup,
    min_max_year_lookup,
)
from models.student_term_record import StudentTermRecord
from models.student_year_record import StudentYearRecord
from models.student import Student
from models.user import User
from models import storage
from api.v1.views import errors


@admin.route("/students/average-range", methods=["GET"])
@admin_required
def student_average_range(admin_data: UserT) -> Tuple[Response, int]:
    """
    Retrieve and return the average range of students.

    Returns:
        Response: A JSON response containing the average range of students.
                  If no students are found, returns a 404 error with an appropriate message.
    """
    try:
        custom_types = {
            **min_max_year_lookup(StudentYearRecord.final_score, "year"),
            **min_max_year_lookup(StudentYearRecord.rank, "rank"),
            **min_max_semester_lookup(1, StudentTermRecord.average, "semester_one"),
            **min_max_semester_lookup(2, StudentTermRecord.average, "semester_two"),
            **min_max_semester_lookup(1, StudentTermRecord.rank, "rank_semester_one"),
            **min_max_semester_lookup(2, StudentTermRecord.rank, "rank_semester_two"),
        }
        query = (
            storage.session.query(
                custom_types["year_min"],
                custom_types["year_max"],
                custom_types["semester_one_min"],
                custom_types["semester_one_max"],
                custom_types["semester_two_min"],
                custom_types["semester_two_max"],
                custom_types["rank_min"],
                custom_types["rank_max"],
                custom_types["rank_semester_one_min"],
                custom_types["rank_semester_one_max"],
                custom_types["rank_semester_two_min"],
                custom_types["rank_semester_two_max"],
            )
            .join(User.students)
            .outerjoin(Student.year_records)
            .outerjoin(StudentYearRecord.semester_records)
            .outerjoin(StudentTermRecord.semesters)
        )

        result = query.one()
        data_to_serialize = {
            "total_average": {
                "min": result.year_min,
                "max": result.year_max,
            },
            "average_semester_one": {
                "min": result.semester_one_min,
                "max": result.semester_one_max,
            },
            "average_semester_two": {
                "min": result.semester_two_min,
                "max": result.semester_two_max,
            },
            "rank": {
                "min": result.rank_min,
                "max": result.rank_max,
            },
            "rank_semester_one": {
                "min": result.rank_semester_one_min,
                "max": result.rank_semester_one_max,
            },
            "rank_semester_two": {
                "min": result.rank_semester_two_min,
                "max": result.rank_semester_two_max,
            },
        }

        # Return the serialized data
        schema = StudentAverageSchema()
        result = schema.dump(data_to_serialize)

        return jsonify(**result), 200
    except ValidationError as e:
        return errors.handle_validation_error(error=e)
    except Exception as e:
        return errors.handle_internal_error(error=e)
