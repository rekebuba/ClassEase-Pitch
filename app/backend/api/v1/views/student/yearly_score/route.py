from typing import Tuple
from flask import Response, jsonify
from sqlalchemy import and_
from api.v1.utils.typing import UserT
from api.v1.views.utils import student_required
from api.v1.views.student import stud
from models.grade import Grade
from models.student_semester_record import StudentSemesterRecord
from models.student_year_record import StudentYearRecord
from models import storage


@stud.route("/yearly_score", methods=["GET"])
@student_required
def student_yearly_scores(student_data: UserT) -> Tuple[Response, int]:
    """
    Generates the student yearly scores data.

    Args:
        student_data (object): An object containing student identifiers such as student_id, grade_id, and section_id.

    Returns:
        Response: A JSON response containing the student's yearly scores, or an error message if the student is not found.
    """

    query = (
        storage.session.query(
            StudentYearRecord.user_id,
            Grade.id,
            Grade.grade,
            StudentSemesterRecord.semesters,
            StudentSemesterRecord.average,
            StudentYearRecord.final_score,
            StudentYearRecord.year,
        )
        .join(Grade, StudentSemesterRecord.grade_id == Grade.id)
        .join(StudentYearRecord, StudentYearRecord.user_id == StudentSemesterRecord.user_id)
        .filter(
            and_(
                StudentSemesterRecord.user_id == student_data.user_id,
                StudentYearRecord.grade_id == StudentSemesterRecord.grade_id,
                StudentYearRecord.year == StudentSemesterRecord.year,
            )
        )
        .order_by(Grade.grade, StudentSemesterRecord.semesters)
    ).all()

    score = {}
    for student_id, grade_id, grade, semester, average, final_score, year in query:
        if grade not in score:
            score[grade] = {
                "student_id": student_id,
                "grade": grade,
                "grade_id": grade_id,
                "final_score": final_score,
                "year": year,
            }
            score[grade]["semester"] = []
        score[grade]["semester"].append({"semester": semester, "average": average})

    return jsonify(score=score), 200
