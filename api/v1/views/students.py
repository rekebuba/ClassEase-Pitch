from flask import Blueprint, request, jsonify
from sqlalchemy import func
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
    date_obj = datetime.strptime(data['date_of_birth'], "%Y-%m-%dT%H:%M:%S.%f")
    existing_student = storage.get_first(
        Student,
        name=data['name'],
        father_name=data['father_name'],
        grand_father_name=data['grand_father_name'],
        date_of_birth=date_obj
    )

    if existing_student:
        return jsonify({"error": "Student already exists"}), 409

    new_student = User(role='Student')
    new_student.hash_password(new_student.id)

    try:
        # Save User first
        # Convert date_of_birth to datetime if it's not already a datetime object
        if isinstance(data['date_of_birth'], str):
            data['date_of_birth'] = datetime.strptime(data['date_of_birth'], "%Y-%m-%dT%H:%M:%S.%f")

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
    grades = storage.get_all(Grade, id=student_data.grade_id)
    grade_names = [grade.grade for grade in grades]

    return jsonify({"grade": grade_names}), 200


@stud.route('/score', methods=['GET'])
@student_or_admin_required
def get_student_score(student_data, admin_data):
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
