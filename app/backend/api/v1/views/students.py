#!/usr/bin/python3
"""Student views module for the API"""

from flask import Blueprint, request, jsonify, url_for
from marshmallow import ValidationError
from models.year import Year
from models.semester import Semester
from models.event import Event
from models import storage
from models.user import User
from models.grade import Grade
from models.student import Student
from models.section import Section
from models.mark_list import MarkList
from models.assessment import Assessment
from models.subject import Subject
from models.stud_semester_record import STUDSemesterRecord
from models.stud_year_record import STUDYearRecord
from api.v1.views.utils import student_required, admin_or_student_required
from urllib.parse import urlparse, parse_qs
from sqlalchemy import update, and_
from datetime import datetime
from api.v1.schemas.schemas import *
from api.v1.views.methods import save_profile, validate_request
from api.v1.schemas.schemas import CourseListSchema
from api.v1.views import errors


stud = Blueprint('stud', __name__, url_prefix='/api/v1/student')


@stud.route('/panel', methods=['GET'])
@student_required
def student_panel_data(student_data):
    """
    Generates the student panel data.

    Args:
        student_data (object): An object containing student identifiers such as student_id, grade_id, and section_id.

    Returns:
        Response: A JSON response containing the student's information, including grade and section, or an error message if the student is not found.
    """

    try:
        query = (
            storage.session.query(User, Student)
            .join(Student, Student.user_id == User.id)
            .filter(User.identification == student_data.identification)
            .first()
        )

        if not query:
            return errors.handle_not_found_error("Student Not Found")

        # Unpack the query result
        user, student = query

        # Serialize the data using the schema
        schema = StudentPanelSchema()
        result = schema.dump({
            "user": user,
            "student": student
        })

        return jsonify(result), 200
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)


@stud.route('/yearly_score', methods=['GET'])
@student_required
def student_yearly_scores(student_data):
    """
    Generates the student yearly scores data.

    Args:
        student_data (object): An object containing student identifiers such as student_id, grade_id, and section_id.

    Returns:
        Response: A JSON response containing the student's yearly scores, or an error message if the student is not found.
    """

    query = (
        storage.session.query(STUDYearRecord.student_id,
                              Grade.id,
                              Grade.name,
                              STUDSemesterRecord.semester,
                              STUDSemesterRecord.average,
                              STUDYearRecord.final_score,
                              STUDYearRecord.year
                              )
        .join(Grade, STUDSemesterRecord.grade_id == Grade.id)
        .join(STUDYearRecord, STUDYearRecord.student_id == STUDSemesterRecord.student_id)
        .filter(and_(STUDSemesterRecord.student_id == student_data.student_id,
                     STUDYearRecord.grade_id == STUDSemesterRecord.grade_id,
                     STUDYearRecord.year == STUDSemesterRecord.year))
        .order_by(Grade.name, STUDSemesterRecord.semester)
    ).all()

    score = {}
    for student_id, grade_id, grade, semester, average, final_score, year in query:
        if grade not in score:
            score[grade] = {"student_id": student_id, "grade": grade, "grade_id": grade_id,
                            "final_score": final_score, "year": year}
            score[grade]['semester'] = []
        score[grade]['semester'].append({
            "semester": semester,
            "average": average
        })

    return jsonify(score=score), 200


@stud.route('/profile', methods=['PUT'])
@student_required
def update_student_profile(student_data):
    """
    Update the profile of a student with the provided data.

    Args:
        student_data (object): The student object whose profile is to be updated.

    Returns:
        Response: A JSON response indicating the result of the update operation.

    The function expects a JSON payload in the request with the following fields:
        - date_of_birth (str): The student's date of birth.
        - father_phone (str): The student's father's phone number.
        - mother_phone (str): The student's mother's phone number.
        - new_password (str, optional): The new password for the student's account.
        - current_password (str, optional): The current password for the student's account (required if new_password is provided).

    The function performs the following checks:
        - Ensures the request payload is a valid JSON.
        - Ensures all required fields (date_of_birth, father_phone, mother_phone) are present in the payload.
        - If a new password is provided, ensures the current password is also provided and is correct.

    The function updates the student's profile and saves the changes to the storage.

    Returns:
        - 400: If the request payload is not a valid JSON or if any required field is missing.
        - 404: If the user associated with the student ID is not found.
        - 400: If the current password is incorrect.
        - 200: If the profile is updated successfully.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    required_data = {
        'date_of_birth',
        'father_phone',
        'mother_phone',
    }

    for field in required_data:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400

    student_data.date_of_birth = data['date_of_birth']
    student_data.father_phone = data['father_phone']
    student_data.mother_phone = data['mother_phone']

    print(student_data)
    if 'new_password' in data:
        if 'current_password' not in data:
            return jsonify({"error": "Missing old password"}), 400
        user = storage.get_first(User, id=student_data.student_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        if not user.check_password(data['current_password']):
            return jsonify({"error": "Incorrect password"}), 400

        user.hash_password(data['new_password'])
    storage.save()

    return jsonify({"message": "Profile Updated Successfully"}), 200


@stud.route('/assigned_grade', methods=['GET'])
@student_required
def get_student_grade(student_data):
    """
    Retrieve the grade(s) associated with a student.

    Args:
        student_data (object): An object containing student information, 
                               specifically the grade_id attribute.

    Returns:
        Response: A JSON response containing a list of grade names and an HTTP status code 200.
    """
    grades = storage.get_all(Grade, id=student_data.grade_id)
    grade_names = [grade.name for grade in grades]

    return jsonify({"grade": grade_names}), 200


@stud.route('/score', methods=['GET'])
@admin_or_student_required
def get_student_score(student_data, admin_data):
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
        return jsonify({"error": "Bad Request"}), 400

    if not student_data:
        if 'student_id' not in data:
            return jsonify({"error": f"Missing student id"}), 400
        student_data = storage.get_first(
            STUDYearRecord, student_id=data['student_id'])

    required_data = {
        'grade',
        'semester',
    }
    student_id = student_data.student_id

    for field in required_data:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400

    grade = storage.get_first(Grade, grade=data['grade'][0])
    if not grade:
        return jsonify({"error": "Grade not found"}), 404

    mark_list = storage.session.query(MarkList).filter(
        MarkList.student_id == student_id,
        MarkList.grade_id == grade.id,
        MarkList.semester == data['semester'][0]
    )

    updated_student_list = {}
    for mark in mark_list:
        subject = storage.get_first(Subject, id=mark.subject_id)
        if subject.id not in updated_student_list:
            assessment = storage.get_first(
                Assessment, student_id=student_id, subject_id=subject.id, semester=data['semester'][0])
            updated_student_list[subject.id] = {
                "subject": subject.name,
                "subject_average": assessment.total,
                "rank": assessment.rank,
                "assessment": []
            }
        updated_student_list[subject.id]['assessment'].append({
            "assessment_type": mark.type,
            "score": mark.score,
            "percentage": mark.percentage,
        })

    student_assessment = list(updated_student_list.values())

    student = storage.get_first(Student, id=student_id)
    average_score = storage.get_first(
        STUDSemesterRecord, student_id=student_id, year=student_data.year, semester=data['semester'][0])

    if not average_score:
        return jsonify({"error": "No data found"}), 404

    student_summary = {
        "student_id": student_id,
        "name": student.name,
        "father_name": student.father_name,
        "grand_father_name": student.grand_father_name,
        "grade": grade.name,
        "semester": data['semester'][0],
        "year": student_data.year,
        "semester_average": average_score.average,
        "rank": average_score.rank,
    }
    return jsonify({
        "student": student_summary,
        "student_assessment": student_assessment,
    }), 200


@stud.route('/course/registration', methods=['GET'])
@student_required
def list_of_course_available(user_data):
    """
    Retrieve the course registration status of a student.

    Args:
        student_data (object): An object containing student information, 
                               specifically the student_id attribute.

    Returns:
        Response: A JSON response containing the course registration status of the student.
    """
    try:
        student_data = storage.session.query(
            Student).filter_by(user_id=user_data.id).first()
        if not student_data.is_active:
            return jsonify({"message": "Student is not active"}), 400

        available_semester = (
            storage.session.query(Semester.name)
            .join(Event, Semester.event_id == Event.id)  # Fix join condition
            .join(Year, Event.year_id == Year.id)
            .filter(
                Semester.name == (
                    1 if student_data.next_grade_id or not student_data.semester_id else 2),
                Year.ethiopian_year == (
                    (int(Year.ethiopian_year) + 1)
                    if student_data.next_grade_id
                    else Year.ethiopian_year
                ),
                Event.registration_start <= datetime.now().date(),
                Event.registration_end >= datetime.now().date(),
            )
            .first()
        )
        if not available_semester:
            return jsonify({"message": "Registration is closed"}), 400

        # Query subjects based on student's next grade
        subjects = (
            storage.session.query(
                Subject.name.label("subject"),
                Subject.code.label("subject_code"),
                Grade.name.label("grade")
            )
            .join(Grade, Grade.id == Subject.grade_id)
            .filter(Grade.id == (student_data.next_grade_id if student_data.next_grade_id else student_data.current_grade_id))
            .all()
        )

        subject_list = [{key: value for key, value in q._asdict().items()}
                        for q in subjects]

        return jsonify({"course": subject_list, "semester": 1}), 200
    except KeyError as e:
        return errors.handle_internal_error(e)


@stud.route('/course/registration', methods=['POST'])
@student_required
def register_course(user_data):
    try:
        data = {
            **request.get_json(),
            "student_id": user_data.identification
        }
        course_schema = CourseListSchema()
        valid_data = course_schema.load(data)

        new_semester_record = STUDSemesterRecord(
            user_id=valid_data.get('user_id'),
            semester_id=valid_data.get('semester_id'),
            grade_id=valid_data.get('grade_id'),
        )
        storage.add(new_semester_record)
        storage.session.flush()

        new_assessment = []
        for form in valid_data['course']:
            new_assessment.append(
                Assessment(
                    user_id=valid_data.get('user_id'),
                    subject_id=form.get('subject_id'),
                    semester_record_id=new_semester_record.id
                )
            )
        storage.session.bulk_save_objects(new_assessment)

        storage.session.execute(
            update(Student)
            .where(Student.user_id == valid_data.get('user_id'))
            .values(
                semester_id=valid_data.get('semester_id'),
                current_grade_id=valid_data.get('grade_id'),
                next_grade_id=None,
                has_passed=False,
                is_registered=True,
                is_active=True,
                updated_at=datetime.utcnow()
            )
        )

        storage.save()

        return jsonify({"message": "Course registration successful!"}), 201
    except ValidationError as e:
        storage.rollback()
        return errors.handle_validation_error(e)
    except Exception as e:
        storage.rollback()
        return errors.handle_internal_error(e)
