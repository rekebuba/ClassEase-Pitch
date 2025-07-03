#!/usr/bin/python3
"""Teacher views module for the API"""

from typing import Tuple
from flask import Response, request, jsonify
from api.v1.utils.typing import UserT
from models import storage
from datetime import datetime
from models.user import User
from models.subject import Subject
from models.assessment import Assessment
from models.mark_list import MarkList
from models.student_term_record import StudentTermRecord
from models.subject_yearly_average import SubjectYearlyAverage
from models.teacher_record import TeachersRecord
from models.student_year_record import StudentYearRecord
from urllib.parse import urlparse, parse_qs
from sqlalchemy import update, and_
from flask import Blueprint
from api.v1.views.utils import (
    admin_or_student_required,
    student_teacher_or_admin_required,
)
from api.v1.views.methods import save_profile


shared = Blueprint("shared", __name__, url_prefix="/api/v1")


@shared.route("/student/assessment", methods=["GET"])
@admin_or_student_required
def student_assessment(user_data: UserT) -> Tuple[Response, int]:
    """
    Retrieve and display a list of assessments for students based on the provided query parameters.
    """
    url = request.url
    parsed_url = urlparse(url)
    data = parse_qs(parsed_url.query)

    required_data = {"student_id", "grade_id", "year"}

    student_id = data["student_id"][0]
    grade_id = data["grade_id"][0]
    year = data["year"][0]
    # Check if required fields are present
    for field in required_data:
        if field not in data:
            return jsonify({"message": f"Missing {field}"}), 400

    query = (
        storage.session.query(
            Assessment.student_id,
            Subject.code,
            Subject.name,
            Assessment.subject_id,
            Assessment.grade_id,
            Assessment.semester,
            Assessment.total,
            Assessment.rank,
            SubjectYearlyAverage.average,
            SubjectYearlyAverage.rank,
            Assessment.year,
        )
        .select_from(Assessment)
        .join(TeachersRecord, TeachersRecord.id == Assessment.teachers_record_id)
        .join(Subject, Assessment.subject_id == Subject.id)
        .join(
            SubjectYearlyAverage,
            and_(
                SubjectYearlyAverage.student_id == Assessment.student_id,
                SubjectYearlyAverage.grade_id == Assessment.grade_id,
                SubjectYearlyAverage.subject_id == Assessment.subject_id,
                SubjectYearlyAverage.year == Assessment.year,
            ),
        )
        .filter(
            Assessment.student_id == student_id,
            Assessment.grade_id == grade_id,
            Assessment.year == year,
        )
        .order_by(Subject.name)
    ).all()

    if not query:
        return jsonify({"message": "Student not found"}), 404

    student_assessment = {}
    for (
        student_id,
        code,
        name,
        subject_id,
        grade_id,
        semester,
        total,
        rank,
        avg_total,
        avg_rank,
        year,
    ) in query:
        if code not in student_assessment:
            # Initialize with placeholders for semesters
            student_assessment[code] = {
                "student_id": student_id,
                "subject": name,
                "subject_id": subject_id,
                "grade_id": grade_id,
                "avg_total": avg_total,
                "avg_rank": avg_rank,
                "year": year,
                "semI": {"total": None, "rank": None},
                "semII": {"total": None, "rank": None},
            }
        if semester == 1:
            student_assessment[code]["semI"] = {"total": total, "rank": rank}
        elif semester == 2:
            student_assessment[code]["semII"] = {"total": total, "rank": rank}

    summary = (
        storage.session.query(
            StudentTermRecord.semesters,
            StudentTermRecord.average,
            StudentTermRecord.rank,
            StudentYearRecord.final_score,
            StudentYearRecord.rank,
        )
        .select_from(StudentTermRecord)
        .join(
            StudentYearRecord,
            and_(
                StudentYearRecord.student_id == StudentTermRecord.student_id,
                StudentYearRecord.grade_id == StudentTermRecord.grade_id,
                StudentYearRecord.year == StudentTermRecord.year,
            ),
        )
        .filter(StudentTermRecord.student_id == student_id)
        .order_by(StudentTermRecord.semesters)
    ).all()

    if not summary:
        return jsonify({"message": "Summary not found"}), 404

    summary_result = {
        "final_score": summary[0][3],
        "final_rank": summary[0][4],
        "semesters": [],
    }

    for semester, semester_average, semester_rank, _, _ in summary:
        summary_result["semesters"].append(
            {
                "semester": semester,
                "semester_average": semester_average,
                "semester_rank": semester_rank,
            }
        )

    return jsonify(
        {"assessment": list(student_assessment.values()), "summary": summary_result}
    ), 200


@shared.route("/student/assessment/detail", methods=["GET"])
@admin_or_student_required
def student_assessment_detail(user_data: UserT) -> Tuple[Response, int]:
    url = request.url
    parsed_url = urlparse(url)
    data = parse_qs(parsed_url.query)

    required_data = {"student_id", "grade_id", "subject_id", "year"}

    for field in required_data:
        if field not in data:
            return jsonify({"message": f"Missing {field}"}), 400

    student_id = data["student_id"][0]
    grade_id = data["grade_id"][0]
    subject_id = data["subject_id"][0]
    year = data["year"][0]

    try:
        query = (
            storage.session.query(
                MarkList.type, MarkList.score, MarkList.percentage, MarkList.semester
            )
            .filter(
                MarkList.student_id == student_id,
                MarkList.grade_id == grade_id,
                MarkList.subject_id == subject_id,
                MarkList.year == year,
            )
            .order_by(MarkList.percentage.asc(), MarkList.type.asc())
        ).all()

        assessment = {}
        for type, score, percentage, semester in query:
            if semester not in assessment:
                assessment[semester] = []
            assessment[semester].append(
                {
                    "assessment_type": type,
                    "score": score,
                    "percentage": percentage,
                }
            )
    except Exception:
        return jsonify({"message": "Failed to retrieve student assessment"}), 500

    return jsonify(assessment), 200


@shared.route("/upload/profile", methods=["POST"])
@student_teacher_or_admin_required
def upload_profile(user_data: UserT) -> Tuple[Response, int]:
    # Check if the request contains a file
    if "profilePicture" not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files["profilePicture"]

    # Check if a file is selected
    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    # Validate file type and save it
    filepath = save_profile(file)

    if filepath:
        # Save the file path to the database
        storage.session.execute(
            update(User)
            .where(User.id == user_data.id)
            .values(image_path=filepath, updated_at=datetime.utcnow())
        )
        storage.save()

        return jsonify({"message": "File uploaded successfully"}), 200
    else:
        return jsonify({"message": "File type not allowed"}), 400
