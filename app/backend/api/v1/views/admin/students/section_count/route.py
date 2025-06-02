from typing import Any, Dict, Tuple

from flask import Response, jsonify
from marshmallow import ValidationError
from sqlalchemy import case, func
from api.v1.utils.typing import UserT
from api.v1.views import errors
from api.v1.views.admin import admins as admin
from api.v1.views.utils import admin_required

from api.v1.views.admin.students.section_count.schema import (
    SectionCountsSchema,
)
from models.section import Section
from models.semester import Semester
from models.stud_semester_record import STUDSemesterRecord
from models import storage


@admin.route("/students/section-counts", methods=["GET"])
@admin_required
def student_section_counts(admin_data: UserT) -> Tuple[Response, int]:
    """
    Retrieve and return the count of students in each section.

    Returns:
        Response: A JSON response containing the count of students in each section.
                  If no students are found, returns a 404 error with an appropriate message.
    """
    try:
        query = (
            storage.session.query(
                Section.section,
                func.count(case((Semester.name == 1, 1), else_=None)).label(
                    "section_semester_one"
                ),
                func.count(case((Semester.name == 2, 1), else_=None)).label(
                    "section_semester_two"
                ),
            )
            .join(STUDSemesterRecord.sections)
            .join(STUDSemesterRecord.semesters)
            .group_by(Section.section)
            .order_by(Section.section)
        ).all()

        # Process results
        result: Dict[str, Dict[str, Any]] = {
            "section_semester_one": {},
            "section_semester_two": {},
        }
        for section, section_I, section_II in query:
            result["section_semester_one"][section] = section_I
            result["section_semester_two"][section] = section_II

        # Return the serialized data
        schema = SectionCountsSchema()
        send_result = schema.dump(result)

        return jsonify(**send_result), 200
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)
