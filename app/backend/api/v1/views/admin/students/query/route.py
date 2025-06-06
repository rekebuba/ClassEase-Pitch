import json
from typing import Any, Dict, List, Tuple

from num2words import num2words

from flask import Response, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.orm import joinedload
from sqlalchemy import ColumnElement, func
from api.v1.utils.typing import (
    BuiltValidFilterDict,
    BuiltValidSortDict,
    PostLoadParam,
    SendAllStudents,
    UserT,
)
from api.v1.views.admin import admins as admin
from api.v1.views.admin.students.query.methods import (
    build_valid_filter,
    build_valid_sort,
    extract_table_id,
    flatten_keys,
)
from api.v1.views.admin.students.query.schema import AllStudentsSchema, ParamSchema
from api.v1.views.methods import make_case_lookup, paginate_query
from api.v1.views.utils import admin_required
from models.grade import Grade
from models.section import Section
from models.semester import Semester
from models.stud_semester_record import STUDSemesterRecord
from models.stud_year_record import STUDYearRecord
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

        # custom_types: Dict[str, ColumnElement[Any]] = {
        #     **make_case_lookup(1, Section.section, "section"),
        #     **make_case_lookup(1, STUDSemesterRecord.average, "average"),
        #     **make_case_lookup(1, STUDSemesterRecord.rank, "rank"),
        # }

        # # custom sort
        # valid_sort: BuiltValidSortDict = build_valid_sort(
        #     valid_data["sort"], custom_types
        # )
        # # custom filter
        # valid_filters: BuiltValidFilterDict = build_valid_filter(
        #     valid_data["filters"], custom_types
        # )

        query = (
            storage.session.query(
                User,
                Student,
                STUDYearRecord,
                Grade,
                func.group_concat(
                    STUDSemesterRecord.average.op("ORDER BY")(Semester.name)
                ).label("average"),
                func.group_concat(
                    STUDSemesterRecord.rank.op("ORDER BY")(Semester.name)
                ).label("rank"),
                func.group_concat(Section.section.op("ORDER BY")(Semester.name)).label(
                    "section"
                ),
                func.group_concat(Semester.name.op("ORDER BY")(Semester.name)).label(
                    "semesters"
                ),
            )
            .join(User.students)  # User → Student
            .outerjoin(Student.year_records)  # Student → STUDYearRecord
            .outerjoin(STUDYearRecord.semester_records)
            .outerjoin(STUDSemesterRecord.sections)  # SemesterRecord → Section
            .outerjoin(STUDSemesterRecord.semesters)  # SemesterRecord → Semester
            .outerjoin(Section.grade)  # Section → Grade
            .group_by(
                User.id,
                Student.id,
                STUDYearRecord.id,
                Grade.id,
            )
            .options(
                joinedload(User.students)
                .joinedload(Student.year_records)
                .joinedload(STUDYearRecord.semester_records)
                .joinedload(STUDSemesterRecord.sections)
                .joinedload(Section.grade)
            )
        )
        # Check if any students are found
        if not query:
            return jsonify({"data": [], "table_id": {}, "pageCount": 1}), 200

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
                "semesters": {
                    f"semester_{num2words(i)}": v
                    for i, v in enumerate(semesters.split(","), start=1)
                }
                if semesters
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
    # except Exception as e:
    #     return errors.handle_internal_error(e)
