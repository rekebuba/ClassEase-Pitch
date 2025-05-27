from typing import Tuple

from flask import Response, jsonify
from marshmallow import ValidationError
from api.v1.views.admin import admins as admin
from api.v1.utils.typing import UserT
from api.v1.views.admin.registered_grade.schema import RegisteredGradesSchema
from api.v1.views.utils import admin_required
from models.grade import Grade
from models.student import Student
from api.v1.views import errors
from models import storage


@admin.route("/registered_grades", methods=["GET"])
@admin_required
def registered_grades(admin_data: UserT) -> Tuple[Response, int]:
    """
    Retrieve and return a list of registered grades.

    Args:
        admin_data (dict): Data related to the admin making the request.

    Returns:
        Response: A JSON response containing a list of registered grades.
    """
    try:
        registered_grades = (
            storage.session.query(Grade)
            .join(Student, Student.current_grade_id == Grade.id)
            .filter(Student.is_registered == True)
            .group_by(Grade.id)
            .all()
        )

        if not registered_grades:
            return errors.handle_not_found_error("No registered grades found")

        schema = RegisteredGradesSchema()
        result = schema.dump(
            {"grades": [grade.to_dict()["grade"] for grade in registered_grades]}
        )

        return jsonify(result), 200
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)
