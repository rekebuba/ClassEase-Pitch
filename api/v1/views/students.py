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
from api.v1.views.utils import student_required
from urllib.parse import urlparse, parse_qs

stud = Blueprint('stud', __name__, url_prefix='/api/v1/student')


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
@student_required
def get_student_score(student_data):
    url = request.url
    parsed_url = urlparse(url)
    data = parse_qs(parsed_url.query)

    if not data:
        return jsonify({"error": "Bad Request"}), 400

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
                "average": assessment.total,
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

    student_summary = {
        "student_id": student_id,
        "name": student.name,
        "father_name": student.father_name,
        "grand_father_name": student.grand_father_name,
        "grade": grade.grade,
        "semester": data['semester'][0],
        "year": student_data.year,
        "average_score": average_score.average,
        "rank": average_score.rank,
    }
    return jsonify({
        "student": student_summary,
        "student_assessment": student_assessment,
    }), 200
