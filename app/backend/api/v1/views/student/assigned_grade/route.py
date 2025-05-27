from typing import Tuple
from flask import Response, jsonify
from api.v1.utils.typing import UserT
from api.v1.views.utils import student_required
from api.v1.views.student import stud
from models.grade import Grade
from models import storage


@stud.route("/assigned_grade", methods=["GET"])
@student_required
def get_student_grade(student_data: UserT) -> Tuple[Response, int]:
    """
    Retrieve the grade(s) associated with a student.

    Args:
        student_data (object): An object containing student information,
                               specifically the grade_id attribute.

    Returns:
        Response: A JSON response containing a list of grade names and an HTTP status code 200.
    """
    grades = storage.get_all(Grade, id=student_data.grade_id)
    grade_names = [grade.grade for grade in grades]

    return jsonify({"grade": grade_names}), 200
