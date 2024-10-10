from flask import request, jsonify
from models import storage
from models.users import User
from models.grade import Grade
from models.student import Student
from models.section import Section
from models.teacher import Teacher
from models.subject import Subject
from models.assessment import Assessment
from models.mark_list import MarkList
from urllib.parse import urlparse, parse_qs
from flask import Blueprint
from api.v1.views.utils import create_teacher_token, teacher_required

teach = Blueprint('teach', __name__, url_prefix='/api/v1/teacher')


@teach.route('/registration', methods=['POST'])
def register_new_teacher():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Not a JSON"}), 404

    # Check if required fields are present
    if 'name' not in data or 'email' not in data:
        return jsonify({"error": "Missing name or email"}), 400

    new_teacher = User(role='Teacher')
    new_teacher.hash_password(new_teacher.id)


    try:
        # Save User first
        storage.add(new_teacher)

        # Create the Teacher object, using the same id
        teacher = Teacher(id=new_teacher.id, name=data['name'], email=data['email'])

        # Save the Teacher object
        storage.add(teacher)
    except Exception as e:
        storage.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Teacher registered successfully!"}), 201


@teach.route('/students/mark_list', methods=['GET'])
@teacher_required
def get_students(teacher_data):
    url = request.url
    parsed_url = urlparse(url)
    data = parse_qs(parsed_url.query)

    if not data:
        return jsonify({"error": "Bad Request"}), 400

    grade = storage.get_first(Grade, grade=data['grade'][0])
    if not grade:
        return jsonify({"error": "Grade not found"}), 404

    section = storage.get_first(
        Section, teacher_id=teacher_data.id, grade_id=grade.id, section=data['section'][0],
        school_year=data['school_year'][0])
    if not section:
        return jsonify({"error": "Section not found"}), 404

    students = storage.get_all(MarkList, grade_id=grade.id, section_id=section.id,
                               teacher_id=teacher_data.id, semester=data['semester'][0],
                               school_year=data['school_year'][0])
    if not students:
        return jsonify({"error": "Student not found"}), 404

    student_list = []
    for student in students:
        student_list.append(student.to_dict())

    return jsonify(student_list), 200


@teach.route('/students/mark_list', methods=['PUT'])
@teacher_required
def add_student_assessment(teacher_data):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 404

    for student in data:
        mark_list = storage.get_first(MarkList, id=student['id'])
        if not mark_list:
            return jsonify({"error": "Student not found"}), 404
        mark_list.score = student['score']
        storage.add(mark_list)

    return jsonify({"message": "Student Mark Updated Successfully!"}), 201


@teach.route('/dashboard', methods=['GET'])
@teacher_required
def teacher_dashboard(teacher_data):
    return jsonify(teacher_data.to_dict()), 200
