import json
from typing import Any, Dict, Tuple

from flask import Response, jsonify
from marshmallow import ValidationError
from sqlalchemy import case, func, select
from sqlalchemy.orm import aliased
from api.v1.utils.typing import UserT
from api.v1.views import errors
from api.v1.views.admin import admins as admin
from api.v1.views.utils import admin_required

from api.v1.views.admin.students.section_count.schema import (
    SectionCountsSchema,
)
from models.section import Section
from models.academic_term import AcademicTerm
from models.student_term_record import StudentTermRecord
from models import storage
from models.student import Student


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
        section_counts = (
            select(
                Section.section.label("section"),
                Semester.name.label("semester"),
                func.count(Student.id.distinct()).label("student_count"),
            )
            .select_from(Student)
            .outerjoin(StudentTermRecord, StudentTermRecord.student_id == Student.id)
            .outerjoin(Section, Section.id == StudentTermRecord.section_id)
            .outerjoin(Semester, Semester.id == StudentTermRecord.semester_id)
            .group_by(Section.section, Semester.name)
        ).subquery()

        sc = aliased(section_counts)

        main_query = (
            select(
                sc.c.section,
                func.group_concat(sc.c.semester.op("ORDER BY")(sc.c.semester)).label(
                    "semester_list"
                ),
                func.group_concat(
                    sc.c.student_count.op("ORDER BY")(sc.c.semester)
                ).label("student_counts"),
            )
            .select_from(sc)
            .group_by(sc.c.section)
            # .order_by(sc.c.section)
        )

        query = storage.session.execute(main_query).all()

        # Process results
        result: Dict[str, Dict[str, Any]] = {
            "section_semester_one": {},
            "section_semester_two": {},
        }
        for section, semester, student_counts in query:
            count = student_counts.split(",") if student_counts else [0, 0]
            if len(count) == 1:
                count.append(count[0])
            if section is None:
                section = "N/A"

            result["section_semester_one"][section] = int(count[0])
            result["section_semester_two"][section] = int(count[1])

        # Return the serialized data
        schema = SectionCountsSchema()
        send_result = schema.dump(result)

        return jsonify(**send_result), 200
    except ValidationError as e:
        return errors.handle_validation_error(error=e)
    except Exception as e:
        return errors.handle_internal_error(error=e)
