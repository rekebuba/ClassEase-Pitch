#!/usr/bin/python3
"""Teacher views module for the API"""

import os
from flask import request, jsonify, current_app, url_for
from marshmallow import ValidationError
from sqlalchemy import func
from models import storage
from datetime import datetime
from models.user import User
from models.admin import Admin
from models.grade import Grade
from models.student import Student
from models.section import Section
from models.subject import Subject
from models.assessment import Assessment
from models.mark_list import MarkList
from models.stud_semester_record import STUDSemesterRecord
from models.average_subject import AVRGSubject
from models.teacher import Teacher
from models.teacher_record import TeachersRecord
from models.stud_year_record import STUDYearRecord
from urllib.parse import urlparse, parse_qs
from sqlalchemy import update, and_
from flask import Blueprint
from api.v1.views.utils import (
    admin_or_student_required,
    student_teacher_or_admin_required,
)
from api.v1.services.user_service import UserService
from api.v1.views.methods import paginate_query
from api.v1.views import errors
from api.v1.schemas.schemas import UserDetailSchema
from models.base_model import BaseModel, CustomTypes
from api.v1.views.methods import save_profile
from werkzeug.utils import secure_filename


shared = Blueprint("shared", __name__, url_prefix="/api/v1")


@shared.route("/registration/<role>", methods=["POST"])
def register_new_user(role):
    """
    Registers a new user (Admin, Student, Teacher) in the system.

    Args:
        role (str): The role of the user to be registered. It should be one of 'Admin', 'Student', or 'Teacher'.

    Returns:
        Response: A JSON response indicating the success or failure of the registration process.
    """
    role = role.lower()
    if role not in ["admin", "student", "teacher"]:
        return jsonify({"message": "Invalid role"}), 400

    try:
        data = request.form.to_dict()  # Get form data as a dictionary
        if not data:
            raise Exception("No data provided")

        data["user"] = {
            "national_id": data.pop("national_id", None),
            "identification": data.pop("identification", None),
            "role": data.pop("role", None),
            "image_path": request.files.get("image_path"),
        }

        result = UserService().create_role_based_user(role, data)
        if not result:
            raise Exception("Failed to register user")

        return {"message": f"{role} registered successfully!"}, 201
    except ValidationError as e:
        storage.rollback()
        return errors.handle_validation_error(e)
    except Exception as e:
        storage.rollback()
        return errors.handle_internal_error(e)


@shared.route("/student/assessment", methods=["GET"])
@admin_or_student_required
def student_assessment(admin_data, student_data):
    """
    Retrieve and display a list of assessments for students based on the provided query parameters.

    Args:
        admin_data (dict): Data related to the admin making the request.

    Returns:
        Response: A JSON response containing the list of student assessments or an error message with the appropriate HTTP status code.

    Query Parameters:
        grade (str): The grade level.
        section (str): The section within the grade.
        year (str): The academic year.

    Responses:
        200: A JSON list of student assessments.
        400: A JSON error message indicating a missing required field.
        404: A JSON error message indicating that the grade, section, subject, or students were not found.
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
            AVRGSubject.average,
            AVRGSubject.rank,
            Assessment.year,
        )
        .select_from(Assessment)
        .join(TeachersRecord, TeachersRecord.id == Assessment.teachers_record_id)
        .join(Subject, Assessment.subject_id == Subject.id)
        .join(
            AVRGSubject,
            and_(
                AVRGSubject.student_id == Assessment.student_id,
                AVRGSubject.grade_id == Assessment.grade_id,
                AVRGSubject.subject_id == Assessment.subject_id,
                AVRGSubject.year == Assessment.year,
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
            student_assessment[code][f"semI"] = {"total": total, "rank": rank}
        elif semester == 2:
            student_assessment[code]["semII"] = {"total": total, "rank": rank}

    summary = (
        storage.session.query(
            STUDSemesterRecord.semester,
            STUDSemesterRecord.average,
            STUDSemesterRecord.rank,
            STUDYearRecord.final_score,
            STUDYearRecord.rank,
        )
        .select_from(STUDSemesterRecord)
        .join(
            STUDYearRecord,
            and_(
                STUDYearRecord.student_id == STUDSemesterRecord.student_id,
                STUDYearRecord.grade_id == STUDSemesterRecord.grade_id,
                STUDYearRecord.year == STUDSemesterRecord.year,
            ),
        )
        .filter(STUDSemesterRecord.student_id == student_id)
        .order_by(STUDSemesterRecord.semester)
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
def student_assessment_detail(admin_data, student_data):
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
    except Exception as e:
        return jsonify({"message": f"Failed to retrieve student assessment"}), 500

    return jsonify(assessment), 200


@shared.route("/upload/profile", methods=["POST"])
@student_teacher_or_admin_required
def upload_profile(student_data, teacher_data, admin_data):
    user = student_data or teacher_data or admin_data
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
        query = storage.session.query(User).filter(User.id == user.id).first()
        query.image_path = filepath
        storage.save()

        return jsonify(
            {
                "message": "File uploaded successfully",
            }
        ), 200
    else:
        return jsonify({"message": "File type not allowed"}), 400


@shared.route("/", methods=["GET"])
@student_teacher_or_admin_required
def user(user):
    try:
        if user.role == CustomTypes.RoleEnum.ADMIN:
            query = (
                storage.session.query(User, Admin)
                .join(Admin, Admin.user_id == User.id)
                .filter(User.identification == user.identification)
                .first()
            )
        elif user.role == CustomTypes.RoleEnum.TEACHER:
            query = (
                storage.session.query(User, Teacher)
                .join(Teacher, Teacher.user_id == User.id)
                .filter(User.identification == user.identification)
                .first()
            )
        elif user.role == CustomTypes.RoleEnum.STUDENT:
            query = (
                storage.session.query(User, Student)
                .join(Student, Student.user_id == User.id)
                .filter(User.identification == user.identification)
                .first()
            )
        if not query:
            return errors.handle_not_found_error("User Not Found")

        user, detail = query
        # Serialize the data using the schema
        schema = UserDetailSchema()
        result = schema.dump({"user": user, "detail": detail})

        return jsonify(result), 200

    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)
