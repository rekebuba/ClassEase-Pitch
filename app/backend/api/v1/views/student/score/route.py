from typing import Tuple
from urllib.parse import parse_qs, urlparse
from flask import Response, jsonify, request
from api.v1.utils.typing import UserT
from api.v1.views.utils import admin_or_student_required
from api.v1.views.student import stud
from models.assessment import Assessment
from models.grade import Grade
from models.mark_list import MarkList
from models.stud_semester_record import STUDSemesterRecord
from models.student import Student
from models.subject import Subject
from models.stud_year_record import STUDYearRecord
from models import storage


@stud.route("/score", methods=["GET"])
@admin_or_student_required
def get_student_score(student_data: UserT) -> Tuple[Response, int]:
    """
    Retrieve and return the score details of a student for a specific grade and semester.

    Args:
        student_data (STUDYearRecord): The yearly record of the student. If not provided, it will be fetched using the student_id from the request query parameters.
        admin_data (dict): Additional data related to the admin making the request (currently unused).

    Returns:
        Response: A JSON response containing the student's score details, including assessments and summary information, or an error message with an appropriate HTTP status code.

    Raises:
        400 Bad Request: If required query parameters are missing or invalid.
        404 Not Found: If the grade or average score data is not found.
    """
    url = request.url
    parsed_url = urlparse(url)
    data = parse_qs(parsed_url.query)

    if not data:
        return jsonify({"message": "Bad Request"}), 400

    if not student_data:
        if "student_id" not in data:
            return jsonify({"message": "Missing student id"}), 400
        student_data = storage.get_first(STUDYearRecord, student_id=data["student_id"])

    required_data = {
        "grade",
        "semester",
    }
    student_id = student_data.student_id

    for field in required_data:
        if field not in data:
            return jsonify({"message": f"Missing {field}"}), 400

    grade = storage.get_first(Grade, grade=data["grade"][0])
    if not grade:
        return jsonify({"message": "Grade not found"}), 404

    mark_list = storage.session.query(MarkList).filter(
        MarkList.student_id == student_id,
        MarkList.grade_id == grade.id,
        MarkList.semester == data["semester"][0],
    )

    updated_student_list = {}
    for mark in mark_list:
        subject = storage.get_first(Subject, id=mark.subject_id)
        if subject.id not in updated_student_list:
            assessment = storage.get_first(
                Assessment,
                student_id=student_id,
                subject_id=subject.id,
                semester=data["semester"][0],
            )
            updated_student_list[subject.id] = {
                "subject": subject.name,
                "subject_average": assessment.total,
                "rank": assessment.rank,
                "assessment": [],
            }
        updated_student_list[subject.id]["assessment"].append(
            {
                "assessment_type": mark.type,
                "score": mark.score,
                "percentage": mark.percentage,
            }
        )

    student_assessment = list(updated_student_list.values())

    student = storage.get_first(Student, id=student_id)
    average_score = storage.get_first(
        STUDSemesterRecord,
        student_id=student_id,
        year=student_data.year,
        semester=data["semester"][0],
    )

    if not average_score:
        return jsonify({"message": "No data found"}), 404

    student_summary = {
        "student_id": student_id,
        "name": student.name,
        "father_name": student.father_name,
        "grand_father_name": student.grand_father_name,
        "grade": grade.grade,
        "semester": data["semester"][0],
        "year": student_data.year,
        "semester_average": average_score.average,
        "rank": average_score.rank,
    }
    return jsonify(
        {
            "student": student_summary,
            "student_assessment": student_assessment,
        }
    ), 200
