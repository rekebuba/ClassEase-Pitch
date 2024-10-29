#!/usr/bin/python3
"""Student views module for the API"""

from flask import Blueprint, request, jsonify
from models import storage
from models.users import User
from models.grade import Grade
from models.student import Student
from models.section import Section
from models.mark_list import MarkList
from models.assessment import Assessment
from models.subject import Subject
from models.average_result import AVRGResult
from models.stud_yearly_record import StudentYearlyRecord
from api.v1.views.utils import student_required, student_or_admin_required
from urllib.parse import urlparse, parse_qs
from datetime import datetime

stud = Blueprint('stud', __name__, url_prefix='/api/v1/student')


@stud.route('/dashboard', methods=['GET'])
@student_required
def student_dashboard(student_data):
    """
    Generates the student dashboard data.

    Args:
        student_data (object): An object containing student identifiers such as student_id, grade_id, and section_id.

    Returns:
        Response: A JSON response containing the student's information, including grade and section, or an error message if the student is not found.
    """
    if not student_data:
        return jsonify({"error": "Student not found"}), 404

    student = storage.get_first(Student, id=student_data.student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    student_dict = student.to_dict()

    grade = storage.get_first(Grade, id=student_data.grade_id)
    student_dict['grade'] = grade.grade if grade else "N/A"

    section = storage.get_first(Section, id=student_data.section_id)
    student_dict['section'] = section.section if section else "N/A"

    return jsonify(student_dict), 200


@stud.route('/update-profile', methods=['PUT'])
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


@stud.route('/registration', methods=['POST'])
def register_new_student():
    """
    Registers a new student in the system.

    This function handles the registration of a new student by validating the input data,
    checking for the existence of required fields, ensuring the uniqueness of the student,
    and saving the student and associated records to the database.

    Returns:
        Response: A JSON response indicating the result of the registration process.

    Possible Responses:
        - 404: If the input data is not a valid JSON.
        - 400: If any required field is missing or if no phone number is provided.
        - 404: If the specified grade is not found.
        - 409: If a student with the same name, father's name, and date of birth already exists.
        - 500: If there is an error during the database operations.
        - 201: If the student is registered successfully.

    Required Fields in JSON Data:
        - name (str): The name of the student.
        - father_name (str): The name of the student's father.
        - grand_father_name (str): The name of the student's grandfather.
        - grade (str): The grade of the student.
        - date_of_birth (str): The date of birth of the student in ISO format.
        - start_year (int): The year the student starts.

    Optional Fields in JSON Data:
        - father_phone (str): The phone number of the student's father.
        - mother_phone (str): The phone number of the student's mother.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Not a JSON"}), 404

    required_data = [
        'name',
        'father_name',
        'grand_father_name',
        'grade',
        'date_of_birth',
        'start_year',
    ]
    # Check if required fields are present
    for field in required_data:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400

    if 'father_phone' not in data and 'mother_phone' not in data:
        return jsonify({"error": "Need to provide at least one phone number"}), 400

    grade = storage.get_first(Grade, grade=data['grade'])
    if not grade:
        return jsonify({"error": "Grade not found"}), 404

    # Check if a student with the same name, father's name, and date of birth already exists
    # date_obj = datetime.strptime(data['date_of_birth'], "%Y-%m-%dT%H:%M:%S.%f")
    # Convert date_of_birth to datetime if it's not already a datetime object
    if isinstance(data['date_of_birth'], str):
        try:
            data['date_of_birth'] = datetime.strptime(
                data['date_of_birth'], "%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
            data['date_of_birth'] = datetime.strptime(
                data['date_of_birth'], "%Y-%m-%d")
    existing_student = storage.get_first(
        Student,
        name=data['name'],
        father_name=data['father_name'],
        grand_father_name=data['grand_father_name'],
        date_of_birth=data['date_of_birth']
    )

    if existing_student:
        return jsonify({"error": "Student already exists"}), 409

    new_student = User(role='Student')
    new_student.hash_password(new_student.id)

    try:
        # Save User first
        # Convert date_of_birth to datetime if it's not already a datetime object
        storage.add(new_student)

        # Create the Student object, using the same id
        student = Student(id=new_student.id, **data)

        new_record = StudentYearlyRecord(
            student_id=student.id, year=data['start_year'], grade_id=grade.id)

        # Save the Student object
        storage.add(student)
        storage.add(new_record)
    except Exception as e:
        storage.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Student registered successfully!"}), 201


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
    grade_names = [grade.grade for grade in grades]

    return jsonify({"grade": grade_names}), 200


@stud.route('/score', methods=['GET'])
@student_or_admin_required
def get_student_score(student_data, admin_data):
    """
    Retrieve and return the score details of a student for a specific grade and semester.

    Args:
        student_data (StudentYearlyRecord): The yearly record of the student. If not provided, it will be fetched using the student_id from the request query parameters.
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
            StudentYearlyRecord, student_id=data['student_id'])

    required_data = {
        'grade',
        'semester',
    }
    student_id = student_data.student_id

    for field in required_data:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400

    print(data['grade'][0])
    grade = storage.get_first(Grade, grade=data['grade'][0])
    if not grade:
        return jsonify({"error": "Grade not found"}), 404

    mark_list = storage.get_session().query(MarkList).filter(
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
        AVRGResult, student_id=student_id, year=student_data.year, semester=data['semester'][0])

    if not average_score:
        return jsonify({"error": "No data found"}), 404

    student_summary = {
        "student_id": student_id,
        "name": student.name,
        "father_name": student.father_name,
        "grand_father_name": student.grand_father_name,
        "grade": grade.grade,
        "semester": data['semester'][0],
        "year": student_data.year,
        "semester_average": average_score.average,
        "rank": average_score.rank,
    }
    return jsonify({
        "student": student_summary,
        "student_assessment": student_assessment,
    }), 200
