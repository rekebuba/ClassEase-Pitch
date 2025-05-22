from typing import Tuple

from flask import Blueprint, Response, jsonify
from sqlalchemy import func
from api.v1.utils.typing import UserT
from api.v1.views.utils import admin_required
from models import storage
from models.teacher import Teacher
from models.student import Student
from models.grade import Grade
from models.subject import Subject
from models.mark_list import MarkList
from models.stud_year_record import STUDYearRecord

admin = Blueprint("admin", __name__, url_prefix="/api/v1/admin")



@admin.route("/overview", methods=["GET"])
@admin_required
def school_overview(admin_data: UserT) -> Tuple[Response, int]:
    """
    Provides an overview of the school including total number of teachers, total number of students,
    enrollment statistics by grade, and performance statistics by subject.

    Args:
        admin_data (dict): Data related to the admin requesting the overview.
    """
    total_teachers = storage.get_all(Teacher)
    total_students = storage.get_all(Student)
    enrollment_by_grade = (
        storage.session.query(Grade.grade, func.count(STUDYearRecord.student_id))
        .join(Grade, STUDYearRecord.grade_id == Grade.id)
        .group_by(
            STUDYearRecord.grade_id,
        )
        .all()
    )

    performance_by_subject = (
        storage.session.query(Subject.name, func.avg(MarkList.score))
        .join(Subject, MarkList.subject_id == Subject.id)
        .group_by(Subject.name)
        .all()
    )

    return jsonify(
        {
            "total_teachers": len(total_teachers),
            "total_students": len(total_students),
            "enrollment_by_grade": [
                {"grade": grade, "student_count": student_count}
                for grade, student_count in enrollment_by_grade
            ],
            "performance_by_subject": [
                {"subject": subject, "average_percentage": average_percentage}
                for subject, average_percentage in performance_by_subject
            ],
        }
    ), 200
