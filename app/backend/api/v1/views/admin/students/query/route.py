from typing import Tuple

from num2words import num2words  # noqa: F401

from flask import Response, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from api.v1.utils.typing import (
    PostLoadParam,
    SendAllStudents,
    UserT,
)
from api.v1.views.admin import admins as admin
from api.v1.views.admin.students.query.methods import (
    extract_table_id,
    flatten_keys,
)
from api.v1.views.admin.students.query.schema import AllStudentsSchema, ParamSchema
from api.v1.views.methods import paginate_query
from api.v1.views.utils import admin_required
from models.grade import Grade
from models.section import Section
from models.semester import Semester
from models.student_semester_record import StudentSemesterRecord
from models.student_year_record import StudentYearRecord
from models.student import Student
from models.user import User
from models import storage
from api.v1.views import errors


@admin.route("/students", methods=["POST"])
@admin_required
def admin_student_list(admin_data: UserT) -> Tuple[Response, int]:
    """
    Retrieve and filter student data based on the provided admin data.

        Response: A JSON response containing the filtered student data, or an error message if any required data is missing or not found.
    """
    try:
        data = request.get_json()
        # Check if required fields are present
        load_schema = ParamSchema()
        valid_data: PostLoadParam = load_schema.load(data)

        query = (
            storage.session.query(
                User,
                Student,
                StudentYearRecord,
                Grade,
                func.group_concat(
                    StudentSemesterRecord.average.op("ORDER BY")(Semester.name)
                ).label("average"),
                func.group_concat(
                    StudentSemesterRecord.rank.op("ORDER BY")(Semester.name)
                ).label("rank"),
                func.group_concat(Section.section.op("ORDER BY")(Semester.name)).label(
                    "section"
                ),
                func.group_concat(Semester.name.op("ORDER BY")(Semester.name)).label(
                    "semesters"
                ),
            )
            .join(User.students)  # User → Student
            .outerjoin(Student.year_records)  # Student → StudentYearRecord
            .outerjoin(StudentYearRecord.semester_records)
            .outerjoin(StudentSemesterRecord.sections)  # SemesterRecord → Section
            .outerjoin(StudentSemesterRecord.semesters)  # SemesterRecord → Semester
            .outerjoin(Section.grade)  # Section → Grade
            .group_by(
                User.id,
                Student.id,
                StudentYearRecord.id,
                Grade.id,
            )
            .options(
                joinedload(User.students)
                .joinedload(Student.year_records)
                .joinedload(StudentYearRecord.semester_records)
                .joinedload(StudentSemesterRecord.sections)
                .joinedload(Section.grade)
            )
        )
        # Check if any students are found
        if not query.all():
            return jsonify({"data": [], "tableId": {}, "pageCount": 1}), 200

        # Use the paginate_query function to handle pagination
        paginated_result = paginate_query(
            query,
            valid_data["page"],
            valid_data["per_page"],
            valid_data["filters"],
            valid_data["sort"],
            valid_data["join_operator"],
        )

        if not paginated_result["items"]:
            return jsonify({"data": [], "tableId": {}, "pageCount": 1}), 200

        # Process results as needed
        data_to_serialize = [
            {
                "user": user.to_dict(),
                "student": student.to_dict(),
                "grade": grade.to_dict() if grade else {},
                "year_record": year_record.to_dict() if year_record else {},
                "averages": {
                    f"average_semester_{num2words(i)}": v
                    for i, v in enumerate(averages.split(","), start=1)
                }
                if averages
                else {},
                "ranks": {
                    f"rank_semester_{num2words(i)}": v
                    for i, v in enumerate(ranks.split(","), start=1)
                }
                if ranks
                else {},
                "sections": {
                    f"section_semester_{num2words(i)}": v
                    for i, v in enumerate(sections.split(","), start=1)
                }
                if sections
                else {},
            }
            for user, student, year_record, grade, averages, ranks, sections, semesters in paginated_result[
                "items"
            ]
        ]

        dump_schema = AllStudentsSchema(many=True)
        result = dump_schema.dump(data_to_serialize)

        modified_result: SendAllStudents = {
            "tableId": extract_table_id(result[0]) if result else {},
            "data": [flatten_keys(item) for item in result],
        }

        # print(json.dumps(modified_result, indent=4, sort_keys=True))

        return jsonify(
            {**modified_result, "pageCount": paginated_result["meta"]["total_pages"]}
        ), 200
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)
