#!/usr/bin/python3
"""Admin views module for the API"""

import json
import os
from flask import request, jsonify, url_for
from marshmallow import ValidationError
from sqlalchemy import func
from models.year import Year
from models import storage
from flask import Blueprint
from models.user import User
from models.admin import Admin
from models.subject import Subject
from models.teacher import Teacher
from models.grade import Grade
from models.student import Student
from models.section import Section
from models.mark_list import MarkList
from models.assessment import Assessment
from models.stud_semester_record import STUDSemesterRecord
from models.average_subject import AVRGSubject
from models.stud_year_record import STUDYearRecord
from models.teacher_record import TeachersRecord
from models.event import Event
from models.semester import Semester
from datetime import datetime
from sqlalchemy import update, select, and_
from urllib.parse import urlparse, parse_qs
from api.v1.views.utils import admin_required
from api.v1.views.methods import save_profile, validate_request
from api.v1.services.event_service import EventService
from api.v1.schemas.schemas import *
from api.v1.services.semester_service import SemesterService
from api.v1.services.admin_service import AdminService
from api.v1.services.user_service import UserService
from api.v1.views import errors


admin = Blueprint('admin', __name__, url_prefix='/api/v1/admin')


@admin.route('/panel', methods=['GET'])
@admin_required
def admin_panel(admin_data):
    """Handle the admin Panel view

    Args:
        admin_data (Admin Instance)

    Returns:
        Response: A JSON response containing the admin data
    """
    try:
        query = (
            storage.session.query(User, Admin)
            .join(Admin, Admin.user_id == User.id)
            .filter(User.identification == admin_data.identification)
            .first()
        )

        if not query:
            return errors.handle_not_found_error("Admin Not Found")

        user, admin = query

        # Serialize the data using the schema
        schema = AdminPanelSchema()
        result = schema.dump({
            "user": user,
            "admin": admin
        })

        return jsonify(result), 200
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)


@admin.route('/profile', methods=['PUT'])
@admin_required
def update_admin_profile(admin_data):
    """
    Update the profile of an admin user.

    Args:
        admin_data (object): The admin user object whose profile is to be updated.

    Returns:
        Response: A JSON response indicating the result of the update operation.

    The function expects a JSON payload in the request with the following fields:
        - name (str): The new name of the admin.
        - email (str): The new email of the admin.
        - current_password (str, optional): The current password of the admin, required if updating the password.
        - new_password (str, optional): The new password for the admin.

    The function performs the following checks:
        - Ensures the request payload is a valid JSON.
        - Ensures the required fields ('name' and 'email') are present in the payload.
        - If updating the password, ensures both 'current_password' and 'new_password' are provided.
        - Verifies the current password before updating to the new password.

    Returns:
        - 400: If the request payload is not a valid JSON or if required fields are missing.
        - 404: If the admin user is not found.
        - 400: If the current password is incorrect.
        - 200: If the profile is updated successfully.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    required_data = {
        'name',
        'email',
        # 'phone',
    }

    for field in required_data:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400

    admin_data.name = data['name']
    admin_data.email = data['email']
    # admin_data.phone = data['phone']

    if 'new_password' in data:
        if 'current_password' not in data:
            return jsonify({"error": "Missing old password"}), 400
        user = storage.get_first(User, id=admin_data.id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        if not user.check_password(data['current_password']):
            return jsonify({"error": "Incorrect password"}), 400

        user.hash_password(data['new_password'])
    storage.save()

    return jsonify({"message": "Profile Updated Successfully"}), 200


@admin.route('/overview', methods=['GET'])
@admin_required
def school_overview(admin_data):
    """
    Provides an overview of the school including total number of teachers, total number of students,
    enrollment statistics by grade, and performance statistics by subject.

    Args:
        admin_data (dict): Data related to the admin requesting the overview.

    Returns:
        Response: A JSON response containing the following keys:
            - total_teachers (int): The total number of teachers.
            - total_students (int): The total number of students.
            - enrollment_by_grade (list): A list of dictionaries, each containing:
                - grade (str): The grade level.
                - student_count (int): The number of students enrolled in that grade.
            - performance_by_subject (list): A list of dictionaries, each containing:
                - subject (str): The name of the subject.
                - average_percentage (float): The average percentage score for that subject.
        HTTP Status Code: 200
    """
    total_teachers = storage.get_all(Teacher)
    total_students = storage.get_all(Student)
    enrollment_by_grade = storage.session.query(
        Grade.name,
        func.count(STUDYearRecord.student_id)
    ).join(Grade, STUDYearRecord.grade_id == Grade.id).group_by(
        STUDYearRecord.grade_id,
    ).all()

    performance_by_subject = storage.session.query(
        Subject.name,
        func.avg(MarkList.score)
    ).join(Subject, MarkList.subject_id == Subject.id).group_by(
        Subject.name
    ).all()

    return jsonify({
        "total_teachers": len(total_teachers),
        "total_students": len(total_students),
        "enrollment_by_grade": [
            {"grade": grade, "student_count": student_count}
            for grade, student_count in enrollment_by_grade
        ],
        "performance_by_subject": [
            {"subject": subject, "average_percentage": average_percentage}
            for subject, average_percentage in performance_by_subject
        ]
    }), 200


@admin.route('/assign-teacher', methods=['PUT'])
@admin_required
def assign_class(admin_data):
    """
    Assigns a teacher to a class based on the provided data.

    Args:
        admin_data (dict): Data containing information about the teacher and class assignment.

    Returns:
        Response: JSON response indicating success or failure of the operation.

    The function performs the following steps:
    1. Parses the JSON request data.
    2. Validates the presence of required fields.
    3. Retrieves the teacher by ID.
    4. Retrieves the grade ID from the Grade table.
    5. Retrieves the subject IDs based on the subjects taught.
    6. Retrieves the section IDs based on the grade and section.
    7. Checks if the teacher is already assigned to the subject and section.
    8. Updates the teacher record if not already assigned.
    9. Updates the MarkList table with the teacher's record ID.
    10. Commits the changes to the database.

    Returns:
        JSON response with a success message and status code 201 if the operation is successful.
        JSON response with an error message and appropriate status code if any validation or database operation fails.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    required_data = [
        'teacher_id',
        'grade',
        'section',
        'subjects_taught',
        'semester',
        'mark_list_year',
    ]
    # Check if required fields are present
    for field in required_data:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400

    # Get the teacher by ID
    teacher = storage.get_first(Teacher, id=data['teacher_id'])
    if not teacher:
        return jsonify({"error": "Teacher not found"}), 404

    # Get the grade_id from the Grade table
    grade_id = storage.session.execute(
        select(Grade.id).where(Grade.name == data['grade'])
    ).scalars().first()
    if not grade_id:
        return jsonify({"error": "No grade found for the teacher"}), 404

    # get the subject_id
    subjects_taught = storage.session.query(Subject).filter(
        Subject.grade_id == grade_id,
        Subject.name.in_(data['subjects_taught'])
    ).all()
    if not subjects_taught:
        return jsonify({"error": "Subject not found"}), 404

    try:
        for subject in subjects_taught:
            # get the section_id
            section_ids = [id[0] for id in storage.session.query(Section.id).filter(
                Section.grade_id == grade_id,
                Section.section.in_(data['section'])
            ).all()]

            if not section_ids:
                return jsonify({"error": f"Section not found, Mark List was not created for the grade {data['grade']}"}), 404

            for section_id in section_ids:
                # check if the another teacher is already assigned to the subject
                teacher_record = storage.get_first(
                    TeachersRecord, grade_id=grade_id, section_id=section_id, subject_id=subject.id, semester=data['semester'])
                # update the teacher record
                if teacher_record:
                    return jsonify({"error": "Teacher already assigned"}), 409
                teacher_record = TeachersRecord(
                    teacher_id=teacher.id,
                    grade_id=grade_id,
                    section_id=section_id,
                    subject_id=subject.id,
                    semester=data['semester']
                )

                storage.add(teacher_record)

                # Update the MarkList table
                storage.session.execute(
                    update(MarkList)
                    .where(and_(
                        MarkList.grade_id == grade_id,
                        MarkList.section_id == section_id,
                        MarkList.subject_id == subject.id,
                        MarkList.semester == data['semester'],
                        MarkList.year == data['mark_list_year']
                    ))
                    .values(teachers_record_id=teacher_record.id)
                )

                # Update the Assessment table
                storage.session.execute(
                    update(Assessment)
                    .where(and_(
                        Assessment.grade_id == grade_id,
                        Assessment.subject_id == subject.id,
                        Assessment.semester == data['semester'],
                        Assessment.year == data['mark_list_year']
                    ))
                    .values(teachers_record_id=teacher_record.id)
                )

                # Update the AVRGSubject table
                storage.session.execute(
                    update(AVRGSubject)
                    .where(and_(
                        AVRGSubject.grade_id == grade_id,
                        AVRGSubject.subject_id == subject.id,
                        AVRGSubject.year == data['mark_list_year']
                    ))
                    .values(teachers_record_id=teacher_record.id)
                )

                # Commit the final updates to the database
                storage.save()
    except Exception as e:
        storage.rollback()
        return jsonify({"error": "error internal server"}), 500

    return jsonify({"message": "Teacher assigned successfully!"}), 201


@admin.route('/events', methods=['GET'])
@admin_required
def available_events(admin_data):
    """
    Handle retrieval of events.

    Args:
        admin_data (object): The admin data object.

    Returns:
        Response: A JSON response list of events or an error message.
    """
    try:
        events = storage.session.query(Event).all()

        if not events:
            return errors.handle_not_found_error("No event found")

        schema = AvailableEventsSchema()
        result = schema.dump({
            "events": events
        })

        return jsonify(result), 200
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)


@admin.route('/event/new', methods=['POST'])
@admin_required
def create_events(admin_data):
    try:
        data = request.get_json()
        event_schema = EventSchema()
        validated_data = event_schema.load(data)

        # extract any nested felids
        semester = validated_data.pop('semester', None)

        new_event = Event(**validated_data)
        storage.add(new_event)
        storage.session.flush()

        if new_event.purpose == 'New Semester':
            semester_data = {
                **semester,
                "event_id": new_event.id,
            }

            # check for duplicate event
            existing_event = (
                storage.session.query(Event, Semester, Year)
                .join(Semester, Semester.event_id == Event.id)
                .join(Year, Year.id == Event.year_id)
                .filter(and_(
                    Event.purpose == new_event.purpose,
                    Event.organizer == new_event.organizer
                ))
            )

            new_semester = Semester(**semester_data)
            storage.add(new_semester)

        storage.save()

        return event_schema.dump({"message": "Event Created Successfully"}), 201
    except ValidationError as e:
        storage.rollback()
        return errors.handle_validation_error(e)
    except Exception as e:
        storage.rollback()
        return errors.handle_internal_error(e)


@admin.route('/registered_grades', methods=['GET'])
@admin_required
def registered_grades(admin_data):
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
            .join(STUDSemesterRecord, STUDSemesterRecord.grade_id == Grade.id)
            .group_by(Grade.id)
            .all()
        )
        if not registered_grades:
            return errors.handle_not_found_error("No registered grades found")

        schema = RegisteredGradesSchema()
        result = schema.dump({
            "grades": [grade.to_dict()['name'] for grade in registered_grades]
        })

        return jsonify(result), 200
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)


@admin.route('/mark-list/new', methods=['POST'])
@admin_required
def create_mark_list(admin_data):
    """
    Create a mark list for students based on the provided data.

    Args:
        admin_data (dict): The data provided by the admin to create the mark list.

    Returns:
        Response: A JSON response indicating the success or failure of the operation.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 404

        mark_list_schema = CreateMarkListSchema()
        validated_data = mark_list_schema.load(data)
        mark_list = []
        for assessment in validated_data['mark_assessment']:
            registered_students = storage.get_all(
                STUDSemesterRecord, grade_id=assessment['grade_id'], semester_id=validated_data['semester_id'])
            for student in registered_students:
                for subject in assessment['subjects']:
                    for assessment_type in assessment['assessment_type']:
                        new_mark_list = MarkList(
                            user_id=student.user_id,
                            semester_record_id=student.id,
                            subject_id=subject['subject_id'],
                            type=assessment_type['type'],
                            percentage=assessment_type['percentage']
                        )

                        mark_list.append(new_mark_list)

        storage.session.bulk_save_objects(mark_list)
        storage.save()

        return jsonify({"message": "Mark list created successfully!"}), 201
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)


@admin.route('/students/mark_list', methods=['GET'])
@admin_required
def show_mark_list(admin_data):
    """
    Retrieve and display a list of marks for students based on the provided query parameters.

    Args:
        admin_data (dict): Data related to the admin making the request.

    Returns:
        Response: A JSON response containing the list of student marks or an error message with the appropriate HTTP status code.

    Query Parameters:
        grade (str): The grade level.
        sections (str): The section within the grade.
        subject (str): The subject for which marks are being requested.
        assessment_type (str): The type of assessment.
        semester (str): The semester for which marks are being requested.
        year (str): The academic year.

    Responses:
        200: A JSON list of student marks.
        400: A JSON error message indicating a missing required field.
        404: A JSON error message indicating that the grade, section, subject, or students were not found.
    """
    url = request.url
    parsed_url = urlparse(url)
    data = parse_qs(parsed_url.query)

    required_data = [
        'grade',
        'sections',
        'subject',
        'assessment_type',
        'semester',
        'year'
    ]
    # Check if required fields are present
    for field in required_data:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400

    grade = storage.get_first(Grade, grade=data['grade'][0])
    if not grade:
        return jsonify({"error": "Grade not found"}), 404

    section = storage.get_first(
        Section, grade_id=grade.id, section=data['section'][0], year=data['year'][0])
    if not section:
        return jsonify({"error": "Section not found"}), 404

    subject = storage.get_first(
        Subject, grade_id=grade.id, name=data['subject'][0])
    if not subject:
        return jsonify({"error": "Subject not found"}), 404

    students = storage.get_all(MarkList, grade_id=grade.id, section_id=section.id,
                               subject_id=subject.id, semester=data['semester'][0],
                               year=data['year'][0])
    if not students:
        return jsonify({"error": "Student not found"}), 404

    student_list = []
    for student in students:
        student_list.append(student.to_dict())

    return jsonify(student_list), 200


@admin.route('/students', methods=['GET'])
@admin_required
def admin_student_list(admin_data):
    """
    Retrieve and filter student data based on the provided admin data.

    Args:
        admin_data (dict): The data provided by the admin to filter student records.

    Returns:
        Response: A JSON response containing the filtered student data, or an error message if any required data is missing or not found.

    The function performs the following steps:
    1. Parses the request URL to extract query parameters.
    2. Checks for the presence of required fields ('grade' and 'year') in the query parameters.
    3. Retrieves the grade information from the storage.
    4. Handles pagination and filtering parameters ('page', 'limit', 'search').
    5. Queries the student records based on the grade and year.
    6. Applies search filters if a search term is provided.
    7. Paginates the query results.
    8. Constructs a list of student summaries, including performance data for each student.
    9. Returns the student data along with pagination metadata and header information.

    Error Handling:
    - Returns a 400 error if any required field is missing.
    - Returns a 404 error if the grade is not found, no students are found, or no mark list is available for the specified grade and year.
    """
    url = request.url
    parsed_url = urlparse(url)
    data = parse_qs(parsed_url.query)

    required_data = {
        'grade',
        'year'
    }

    # Check if required fields are present
    for field in required_data:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400

    grade = storage.get_first(Grade, grade=data['grade'][0])
    if not grade:
        return jsonify({"error": "Grade not found"}), 404

    query = (
        storage.session.query(Student.id.label('student_id'),
                              Student.name,
                              Student.father_name,
                              Student.grand_father_name,
                              Section.section,
                              Section.id,
                              STUDYearRecord.grade_id,
                              STUDYearRecord.final_score,
                              STUDYearRecord.rank,
                              STUDYearRecord.year,
                              User.image_path
                              )
        .select_from(STUDYearRecord)
        .join(Student, Student.id == STUDYearRecord.student_id)
        .join(User, User.id == Student.id)
        .join(Section, Section.id == STUDYearRecord.section_id)
        .filter(
            STUDYearRecord.grade_id == grade.id,
            STUDYearRecord.year == data['year'][0]
        )
        .order_by(Section.section.asc(), Student.name.asc(), Student.father_name.asc(), Student.grand_father_name.asc(), Student.id.asc())
    ).all()

    # Check if any students are found
    if not query:
        return jsonify({"error": "No student found"}), 404

    student_list = [{key: url_for('static', filename=value, _external=True)
                     if key == 'image_path' and value is not None else value for key, value in q._asdict().items()} for q in query]

    return jsonify({
        "students": student_list,
        "meta": {},
        "header": {"grade": data['grade'][0], "year": data['year'][0]}
    }), 200


@admin.route('/teachers', methods=['GET'])
@admin_required
def all_teachers(admin_data):
    """
    Retrieve and return a list of teachers with pagination and optional search functionality.

    Args:
        admin_data (dict): Data related to the admin making the request.

    Returns:
        Response: A JSON response containing a list of teachers and pagination metadata.
                  If no teachers are found, returns a 404 error with an appropriate message.

    Query Parameters:
        page (int, optional): The page number for pagination. Defaults to 1.
        limit (int, optional): The number of items per page for pagination. Defaults to 10.
        search (str, optional): A search term to filter teachers by id, first name, last name, email, or phone.

    Raises:
        404: If no teachers are found or if no teachers match the search criteria.
    """
    url = request.url
    parsed_url = urlparse(url)
    data = parse_qs(parsed_url.query)

    query = (
        storage.session.query(Teacher.id,
                              Teacher.first_name.label('firstName'),
                              Teacher.last_name.label('lastName'),
                              Teacher.email,
                              Teacher.no_of_mark_list.label('markList'),
                              User.image_path
                              )
        .join(User, User.id == Teacher.id)
        .group_by(Teacher.id)
    )

    if not query:
        return jsonify({"error": "No teachers found"}), 404

    teacher_list = [{key: url_for('static', filename=value, _external=True)
                     if key == 'image_path' and value is not None else value for key, value in q._asdict().items()} for q in query]

    return jsonify({
        "teachers": teacher_list,
    }), 200
