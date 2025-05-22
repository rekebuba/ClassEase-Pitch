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
from models.stud_semester_record import STUDSemesterRecord
from models.stud_year_record import STUDYearRecord
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
            **min_max_year_lookup(STUDYearRecord.final_score, "year"),
            **min_max_year_lookup(STUDYearRecord.rank, "rank"),
            **min_max_semester_lookup(1, STUDSemesterRecord.average, "semester_I"),
            **min_max_semester_lookup(2, STUDSemesterRecord.average, "semester_II"),
            **min_max_semester_lookup(1, STUDSemesterRecord.rank, "rank_I"),
            **min_max_semester_lookup(2, STUDSemesterRecord.rank, "rank_II"),
        }
        query = (
            storage.session.query(
                custom_types["year_min"],
                custom_types["year_max"],
                custom_types["semester_I_min"],
                custom_types["semester_I_max"],
                custom_types["semester_II_min"],
                custom_types["semester_II_max"],
                custom_types["rank_min"],
                custom_types["rank_max"],
                custom_types["rank_I_min"],
                custom_types["rank_I_max"],
                custom_types["rank_II_min"],
                custom_types["rank_II_max"],
            )
            .join(User.students)
            .outerjoin(Student.year_records)
            .outerjoin(STUDYearRecord.semester_records)
            .outerjoin(STUDSemesterRecord.semesters)
        )

        result = query.one()
        data_to_serialize = {
            "total_average": {
                "min": result.year_min,
                "max": result.year_max,
            },
            "averageI": {
                "min": result.semester_I_min,
                "max": result.semester_I_min,
            },
            "averageII": {
                "min": result.semester_II_min,
                "max": result.semester_II_min,
            },
            "rank": {
                "min": result.rank_min,
                "max": result.rank_max,
            },
            "rankI": {
                "min": result.rank_I_min,
                "max": result.rank_I_max,
            },
            "rankII": {
                "min": result.rank_II_min,
                "max": result.rank_II_max,
            },
        }

        # Return the serialized data
        schema = StudentAverageSchema()
        result = schema.dump(data_to_serialize)

        return jsonify(**result), 200
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)
