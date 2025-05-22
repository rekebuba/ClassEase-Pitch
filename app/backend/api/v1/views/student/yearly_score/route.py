from typing import Tuple
from flask import Response, jsonify
from sqlalchemy import and_
from api.v1.utils.typing import UserT
from api.v1.views.utils import student_required
from api.v1.views.student import stud
from models.grade import Grade
from models.stud_semester_record import STUDSemesterRecord
from models.stud_year_record import STUDYearRecord
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
            STUDYearRecord.user_id,
            Grade.id,
            Grade.grade,
            STUDSemesterRecord.semester,
            STUDSemesterRecord.average,
            STUDYearRecord.final_score,
            STUDYearRecord.year,
        )
        .join(Grade, STUDSemesterRecord.grade_id == Grade.id)
        .join(STUDYearRecord, STUDYearRecord.user_id == STUDSemesterRecord.user_id)
        .filter(
            and_(
                STUDSemesterRecord.user_id == student_data.user_id,
                STUDYearRecord.grade_id == STUDSemesterRecord.grade_id,
                STUDYearRecord.year == STUDSemesterRecord.year,
            )
        )
        .order_by(Grade.grade, STUDSemesterRecord.semester)
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
