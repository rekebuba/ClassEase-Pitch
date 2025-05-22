from typing import Tuple

from flask import Response, jsonify, request
from marshmallow import ValidationError
from sqlalchemy import and_
from api.v1.utils.typing import UserT
from api.v1.views.admin import admins as admin
from api.v1.views.utils import admin_required
from api.v1.views.admin.mark_list.schema import CreateMarkListSchema
from models.student import Student
from models.mark_list import MarkList
from models.stud_semester_record import STUDSemesterRecord
from api.v1.views import errors
from models import storage


@admin.route("/mark-list/new", methods=["POST"])
@admin_required
def create_mark_list(admin_data: UserT) -> Tuple[Response, int]:
    """
    Create a mark list for students based on the provided data.

    Args:
        admin_data (dict): The data provided by the admin to create the mark list.

    Returns:
        Response: A JSON response indicating the success or failure of the operation.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Not a JSON"}), 404

        mark_list_schema = CreateMarkListSchema()
        validated_data = mark_list_schema.load(data)
        mark_list = []
        for assessment in validated_data["mark_assessment"]:
            registered_students = (
                storage.session.query(STUDSemesterRecord.id, Student.user_id)
                .join(STUDSemesterRecord.students)
                .filter(
                    and_(
                        STUDSemesterRecord.semester_id == validated_data["semester_id"],
                        Student.current_grade_id == assessment["grade_id"],
                    )
                )
                .all()
            )
            for semester_record_id, user_id in registered_students:
                for subject in assessment["subjects"]:
                    for assessment_type in assessment["assessment_type"]:
                        new_mark_list = MarkList(
                            user_id=user_id,
                            semester_record_id=semester_record_id,
                            subject_id=subject["subject_id"],
                            type=assessment_type["type"],
                            percentage=assessment_type["percentage"],
                        )

                        mark_list.append(new_mark_list)

        storage.session.bulk_save_objects(mark_list)
        storage.save()

        return jsonify({"message": "Mark list created successfully!"}), 201
    except ValidationError as e:
        return errors.handle_validation_error(e)
    # except Exception as e:
    #     return errors.handle_internal_error(e)
