from typing import Tuple

from flask import Response, jsonify
from sqlalchemy import case, func
from api.v1.utils.typing import UserT
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
    query = (
        storage.session.query(
            Section.section,
            func.count(case((Semester.name == 1, 1), else_=None)).label("section_I"),
            func.count(case((Semester.name == 2, 1), else_=None)).label("section_II"),
        )
        .join(STUDSemesterRecord.sections)
        .join(STUDSemesterRecord.semesters)
        .group_by(Section.section)
        .order_by(Section.section)
    )
    # Process results
    result = query.all()

    data_to_serialize = [
        {
            "sectionI": {"section": section, "total": section_I},
            "sectionII": {"section": section, "total": section_II},
        }
        for section, section_I, section_II in result
    ]

    # Return the serialized data
    schema = SectionCountsSchema(many=True)
    send_result = schema.dump(data_to_serialize)

    return jsonify(**send_result), 200
