from flask import request, jsonify
from models import storage
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

    teacher = Teacher(name=data['name'], email=data['email'])
    teacher.hash_password(data['password'])
    storage.add(teacher)

    return jsonify({"message": "Teacher registered successfully!"}), 201


@teach.route('/login', methods=['POST'])
def teacher_login():
    data = request.get_json()

    user = storage.get_first(Teacher, email=data['email'])
    if user and user.check_password(data['password']):
        access_token = create_teacher_token(user.id)
        return jsonify(access_token=access_token), 200

    return jsonify({"error": "Invalid credentials"}), 401


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
        Section, teacher_id=teacher_data.id, grade_id=grade.id, section=data['section'][0])
    if not section:
        return jsonify({"error": "Section not found"}), 404

    students = storage.get_all(MarkList, grade_id=grade.id, section_id=section.id,
                               teacher_id=teacher_data.id, semester=data['semester'][0])
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
