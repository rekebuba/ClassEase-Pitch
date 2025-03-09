#!/usr/bin/python3
"""Admin views module for the API"""

import os
from flask import request, jsonify, url_for
from marshmallow import ValidationError
from sqlalchemy import func
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
from models.average_result import AVRGResult
from models.average_subject import AVRGSubject
from models.stud_yearly_record import StudentYearlyRecord
from models.teacher_record import TeachersRecord
from models.event import Event
from models.semester import Semester
from datetime import datetime
from sqlalchemy import update, select, and_
from urllib.parse import urlparse, parse_qs
from api.v1.views.utils import admin_required
from api.v1.views.methods import save_profile, validate_request
from api.v1.services.event_service import EventService
from api.v1.schemas.admin.registration_schema import AdminRegistrationSchema
from api.v1.schemas.user.registration_schema import UserRegistrationSchema
from api.v1.services.semester_service import SemesterService
from api.v1.schemas.event.create_schema import EventCreationSchema
from api.v1.services.admin_service import AdminService
from api.v1.schemas.semester.create_schema import SemesterCreationSchema
from api.v1.services.user_service import UserService
from api.v1.views import errors
admin = Blueprint('admin', __name__, url_prefix='/api/v1/admin')


@admin.route('/dashboard', methods=['GET'])
@admin_required
def admin_dashboard(admin_data):
    """
    Handle the admin dashboard view.

    Args:
        admin_data (object): The admin data object. It should have a method `to_dict()` 
                             that converts the object to a dictionary.

    Returns:
        tuple: A tuple containing a JSON response and an HTTP status code.
               - If `admin_data` is None, returns a JSON response with an error message 
                 and a 404 status code.
               - If `admin_data` is valid, returns a JSON response with the admin data 
                 dictionary and a 200 status code.
    """
    query = (storage.session.query(User.image_path)
             .join(Admin, Admin.id == User.id)
             .filter(Admin.id == admin_data.id)
             ).first()

    filename = query[0]

    image_url = url_for('static', filename=f'{filename}', _external=True)

    return jsonify({
        **(admin_data.to_dict()),
        "image_url": image_url
    }), 200


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
        func.count(StudentYearlyRecord.student_id)
    ).join(Grade, StudentYearlyRecord.grade_id == Grade.id).group_by(
        StudentYearlyRecord.grade_id,
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
def events(admin_data):
    """
    Handle the creation and retrieval of events.

    Args:
        admin_data (object): The admin data object.

    Returns:
        Response: A JSON response containing the list of events or an error message with the appropriate HTTP status code.
    """

    semesters = storage.session.query(Semester).all()

    if not semesters:
        return jsonify({"error": "No events found"}), 404

    # Convert DateTime fields to string (YYYY-MM-DD) before sending
    formatted_semesters = [
        {
            "id": sem.id,
            "name": sem.name,
            "academicYearEC": sem.academic_year_EC,
            "startDate": sem.start_date.strftime("%Y-%m-%d"),
            "endDate": sem.end_date.strftime("%Y-%m-%d"),
            "registrationStart": sem.registration_start.strftime("%Y-%m-%d"),
            "registrationEnd": sem.registration_end.strftime("%Y-%m-%d"),
        }
        for sem in semesters
    ]
    return jsonify(formatted_semesters), 200


@admin.route('/event/new', methods=['POST'])
@admin_required
def create_events(admin_data):
    try:
        data = request.get_json()
        event_schema = EventCreationSchema()
        validated_data = event_schema.load(data)

        new_event = EventService.create_event(**validated_data)
        storage.add(new_event)
        storage.session.flush()

        if new_event.purpose == 'New Semester':
            semester_data = {
                **data.get('semester'),
                "event_id": new_event.id,
            }

            semester_schema = SemesterCreationSchema()
            valid_semester_data = semester_schema.load(semester_data)

            new_semester = SemesterService.create_semester(
                **valid_semester_data)
            storage.add(new_semester)

        storage.save()

        return event_schema.dump({"message": "Event Created Successfully"}), 201
    except ValidationError as e:
        print(e.messages)
        errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)


@admin.route('/students/mark_list', methods=['PUT'])
@admin_required
def create_mark_list(admin_data):
    """
    Create a mark list for students based on the provided admin data.

    Args:
        admin_data (dict): The data provided by the admin to create the mark list.

    Returns:
        Response: A JSON response indicating the success or failure of the operation.

    The function performs the following steps:
    1. Parses the JSON request data.
    2. Validates the presence and types of required fields.
    3. Retrieves the grade ID from the Grade table.
    4. Updates the Section table with the provided sections.
    5. Checks if a mark list already exists for the given grade, section, semester, and year.
    6. Retrieves students for the given grade and year.
    7. Assigns sections to students who do not have one.
    8. Updates the Subject table with the provided subjects.
    9. Creates mark list, assessment, and average result objects for each student.
    10. Saves the created objects to the database.

    Returns:
        Response: A JSON response indicating the success or failure of the operation.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 404

    required_data = {
        'grade',
        'sections',
        'subjects',
        'assessment_type',
        'semester',
        'year'
    }

    # Check if required fields are present
    for field in required_data:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400
        elif field in {'grade', 'section', 'semester'} and type(data[field]) != int:
            return jsonify({"error": f"{field} must be an integer"}), 400
        elif field == 'assessment_type':
            for assessment in data[field]:
                if assessment.keys() != {'type', 'percentage'}:
                    return jsonify({"error": "Missing type or percentage"}), 400
                elif type(assessment['type']) != str or type(assessment['percentage']) != int:
                    return jsonify({"error": "Type must be a string and percentage must be an integer"}), 400

    # Get the grade_id from the Grade table
    grade = storage.get_first(Grade, grade=data['grade'])

    if not grade:
        return jsonify({"error": "Grade not found"}), 404
    else:
        grade_id = grade.id

    # Update the Section table
    existing_sections = {}
    for section in data['sections']:
        exists = storage.get_first(
            Section, grade_id=grade_id, section=section)
        if exists and storage.get_first(MarkList, section_id=exists.id, year=data['year']):
            existing_sections[section] = exists.id
        elif not exists:
            section = Section(grade_id=grade_id, section=section)
            storage.add(section)

    mark_list_exists = (
        storage.session.query(MarkList)
        .filter(MarkList.grade_id == grade_id,
                MarkList.semester == data['semester'],
                MarkList.year == data['year'],
                MarkList.section_id.in_(list(existing_sections.values())))
        .all()
    )

    if mark_list_exists:
        return jsonify({
            "error": f"Mark list already exists for grade = {data['grade']}, "
            f"Section = {' and '.join(map(str, list(existing_sections.keys())))}, "
            f"Semester = {data['semester']}, "
            f"School Year = {data['year']}"
        }), 400

    try:
        students = (
            storage.session.query(StudentYearlyRecord)
            .filter(StudentYearlyRecord.grade_id == grade_id, StudentYearlyRecord.year == data['year'])
            .all()
        )

        if not students:
            return jsonify({"error": f"No students found for the year {data['year']}"}), 404

        # Assign a section randomly to students who do not have one
        for student in students:
            if not student.section_id:
                section = storage.get_random(Section, grade_id=grade_id)
                if not section:
                    return jsonify({"error": "Section not found"}), 404
                update_result = storage.session.execute(
                    update(StudentYearlyRecord)
                    .where(StudentYearlyRecord.student_id == student.student_id)
                    .values(section_id=section.id)
                )

                if update_result.rowcount == 0:
                    return jsonify({"error": f"Failed to update section for student {student.student_id}"}), 500

        storage.save()

        # Update the Subject table
        for course in data['subjects']:
            query = storage.get_first(Subject, grade_id=grade_id, name=course)
            if not query:
                # Tokenize the subject name by spaces and join the first 3 characters of each word
                code = ''.join([word[:2 if len(course.split()) > 1 else 3].upper()
                                for word in course.split()]) + str(data['grade'])
                subject_code = storage.get_first(
                    Subject, code=code, grade_id=grade_id, name=course)
                if subject_code:
                    code = code + 'I'
                new_subject = Subject(name=course, code=code,
                                      grade_id=grade_id, year=data['year'])
                storage.add(new_subject)

        mark_lists = []  # A list to hold mark_list objects
        assessments = []  # A list to hold assessment objects
        average_subject = []
        average_result = []

        for student in students:
            subjects = storage.get_all(Subject, grade_id=grade_id)
            if not subjects:
                return jsonify({"error": "Subjects for the current grade not found"}), 404
            for subject in subjects:
                for assessment_type in data['assessment_type']:
                    values = {
                        "student_id": student.student_id,
                        "grade_id": grade_id,
                        "section_id": student.section_id,
                        "subject_id": subject.id,
                        "semester": data['semester'],
                        "year": data['year'],
                    }
                    mark_lists.append(MarkList(**values, **assessment_type))
                assessments.append(
                    Assessment(student_id=student.student_id,
                               grade_id=grade_id,
                               subject_id=subject.id,
                               section_id=student.section_id,
                               semester=data['semester'],
                               year=data['year']
                               )
                )

                avg_subject = storage.get_first(AVRGSubject,
                                                student_id=student.student_id,
                                                grade_id=grade_id,
                                                subject_id=subject.id,
                                                section_id=student.section_id,
                                                year=data['year']
                                                )
                if not avg_subject:
                    average_subject.append(
                        AVRGSubject(
                            student_id=student.student_id,
                            grade_id=grade_id,
                            subject_id=subject.id,
                            section_id=student.section_id,
                            year=data['year']
                        ))

            average_result.append(
                AVRGResult(student_id=student.student_id,
                           grade_id=grade_id,
                           section_id=student.section_id,
                           semester=data['semester'],
                           year=data['year']
                           )
            )

        # Save the objects to the database
        storage.session.bulk_save_objects(mark_lists)
        storage.session.bulk_save_objects(assessments)
        storage.session.bulk_save_objects(average_result)
        if average_subject:
            storage.session.bulk_save_objects(average_subject)

        storage.save()
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Mark list created successfully!"}), 201


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
                              StudentYearlyRecord.grade_id,
                              StudentYearlyRecord.final_score,
                              StudentYearlyRecord.rank,
                              StudentYearlyRecord.year,
                              User.image_path
                              )
        .select_from(StudentYearlyRecord)
        .join(Student, Student.id == StudentYearlyRecord.student_id)
        .join(User, User.id == Student.id)
        .join(Section, Section.id == StudentYearlyRecord.section_id)
        .filter(
            StudentYearlyRecord.grade_id == grade.id,
            StudentYearlyRecord.year == data['year'][0]
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
