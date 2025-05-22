from typing import Tuple

from flask import Response, jsonify, request
from api.v1.utils.typing import UserT
from api.v1.views.admin import admins as admin
from api.v1.views.utils import admin_required
from urllib.parse import urlparse, parse_qs

from models.grade import Grade
from models.mark_list import MarkList
from models.section import Section
from models.subject import Subject
from models import storage


@admin.route("/students/mark_list", methods=["GET"])
@admin_required
def show_mark_list(admin_data: UserT) -> Tuple[Response, int]:
    """
    Retrieve and display a list of marks for students based on the provided query parameters.

    Args:
        admin_data (dict): Data related to the admin making the request.

    Returns:
        Response: A JSON response containing the list of student marks or an error message with the appropriate HTTP status code.
    """
    url = request.url
    parsed_url = urlparse(url)
    data = parse_qs(parsed_url.query)

    required_data = [
        "grade",
        "sections",
        "subject",
        "assessment_type",
        "semester",
        "year",
    ]
    # Check if required fields are present
    for field in required_data:
        if field not in data:
            return jsonify({"message": f"Missing {field}"}), 400

    grade = storage.get_first(Grade, grade=data["grade"][0])
    if not grade:
        return jsonify({"message": "Grade not found"}), 404

    section = storage.get_first(
        Section, grade_id=grade.id, section=data["section"][0], year=data["year"][0]
    )
    if not section:
        return jsonify({"message": "Section not found"}), 404

    subject = storage.get_first(Subject, grade_id=grade.id, name=data["subject"][0])
    if not subject:
        return jsonify({"message": "Subject not found"}), 404

    students = storage.get_all(
        MarkList,
        grade_id=grade.id,
        section_id=section.id,
        subject_id=subject.id,
        semester=data["semester"][0],
        year=data["year"][0],
    )
    if not students:
        return jsonify({"message": "Student not found"}), 404

    student_list = []
    for student in students:
        student_list.append(student.to_dict())

    return jsonify(student_list), 200
