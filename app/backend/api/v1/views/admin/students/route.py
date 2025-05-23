from typing import Any, List, Tuple

from flask import Response, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.orm import joinedload
from sqlalchemy import ColumnElement
from api.v1.utils.typing import UserT
from api.v1.views.admin import admins as admin
from api.v1.views.admin.students.schema import AllStudentsSchema, ParamSchema
from api.v1.views.methods import make_case_lookup, paginate_query
from api.v1.views.utils import admin_required
from api.v1.schemas.config_schema import OPERATOR_MAPPING
from models.grade import Grade
from models.section import Section
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
        schema = ParamSchema()
        valid_data = schema.load(data)

        custom_types = {
            **make_case_lookup(1, Section.section, "section"),
            **make_case_lookup(1, STUDSemesterRecord.average, "average"),
            **make_case_lookup(1, STUDSemesterRecord.rank, "rank"),
        }

        # custom sort
        for custom_sort in valid_data["custom_sorts"]:
            column_name = custom_sort["column_name"]
            is_desc = custom_sort.get("desc", False)

            expr = custom_types.get(column_name)
            if expr is None:
                raise ValidationError(f"Invalid custom sort: {custom_sort}")

            valid_data["valid_sorts"].append(expr.desc() if is_desc else expr)

        # custom filter
        result: List[ColumnElement[Any]] = []
        for custom_filter in valid_data["custom_filters"]:
            column_name = custom_filter["column_name"]
            operator = custom_filter["operator"]
            value = custom_filter["value"]

            expr = custom_types.get(column_name)
            if expr is None:
                raise ValidationError(f"Invalid custom filter: {custom_filter}")

            op_func = OPERATOR_MAPPING.get(operator)
            if op_func is None:
                raise ValidationError(f"Unsupported operator: {operator}")

            try:
                condition = op_func(expr, value)
            except Exception as e:
                raise ValidationError(f"Invalid value for operator '{operator}': {e}")

            result.append(condition)

        valid_data["custom_filters"] = result

        print("valid_data: ", valid_data)

        query = (
            storage.session.query(
                User,
                Student,
                STUDYearRecord,
                Grade,
                custom_types["sectionI"],
                custom_types["sectionII"],
                custom_types["averageI"],
                custom_types["averageII"],
                custom_types["rankI"],
                custom_types["rankII"],
            )
            .join(User.students)  # User → Student
            .outerjoin(Student.year_records)  # Student → STUDYearRecord
            .outerjoin(STUDYearRecord.semester_records)
            .outerjoin(STUDSemesterRecord.sections)  # SemesterRecord → Section
            # SemesterRecord → Semester
            .outerjoin(STUDSemesterRecord.semesters)
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
            valid_data["valid_filters"],
            valid_data["custom_filters"],
            valid_data["valid_sorts"],
            valid_data["join_operator"],
        )

        if not paginated_result["items"]:
            return jsonify({"data": [], "table_id": {}, "pageCount": 1}), 200

        # Process results as needed
        data_to_serialize = [
            {
                "user": user.to_dict(),
                "student": student.to_dict(),
                "grade": grade.to_dict(),
                "year_record": year_record.to_dict(),
                "sectionI": section_I,
                "sectionII": section_II,
                "averageI": average_I,
                "averageII": average_II,
                "rankI": rank_I,
                "rankII": rank_II,
            }
            for user, student, year_record, grade, section_I, section_II, average_I, average_II, rank_I, rank_II in paginated_result[
                "items"
            ]
        ]

        schema = AllStudentsSchema(many=True)
        result = schema.dump(data_to_serialize)
        return jsonify(
            {**result, "pageCount": paginated_result["meta"]["total_pages"]}
        ), 200
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)
