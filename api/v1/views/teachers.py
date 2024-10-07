from flask import request, jsonify, abort
from models import storage
from models.users import User
from models.grade import Grade
from models.student import Student
from models.section import Section
from models.teacher import Teacher
from models.subject import Subject
from models.assessment import Assessment
from models.mark_list import MarkList
from api.v1.views import app_views, teach
from functools import wraps
from urllib.parse import urlparse, parse_qs
import jwt
import os

# Decorator for teacher JWT verification
def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]  # Bearer token

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, os.getenv("TEACHER_JWT_SECRET"), algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Teacher token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid Teacher token'}), 401

        return f(*args, **kwargs)

    return decorated_function

@teach.route('/registration', methods=['POST'])
def register_new_teacher():
    data = request.get_json()

    if not data:
        abort(400, description="Not a JSON")

    teacher = Teacher(name=data['name'], email=data['email'])
    teacher.hash_password(data['password'])
    storage.add(teacher)

    return  jsonify({"message": "Teacher registered successfully!"}), 201


@teach.route('/students/mark_list', methods=['GET'])
@teacher_required
def get_students():
    url = request.url
    parsed_url = urlparse(url)
    data = parse_qs(parsed_url.query)

    if not data:
        abort(400, description="Bad Request!")

    token = request.headers['Authorization'].split(" ")[1]  # Bearer <token>
    payload = jwt.decode(token, os.getenv("TEACHER_JWT_SECRET"), algorithms=["HS256"])
    teacher_id = payload['teacher_id']

    grade = storage._DBStorage__session.query(Grade).filter_by(grade=data['grade']).first()
    if not grade:
        abort(404, description="Grade not found")

    section = storage._DBStorage__session.query(Section).filter_by(teacher_id=teacher_id, grade_id=grade.id, section=data['section']).first()
    if not section:
            abort(404, description="Section not found")

    students = storage._DBStorage__session.query(MarkList).filter_by(grade_id=grade.id, section_id=section.id, teacher_id=teacher_id, semester=data['semester']).all()
    if not students:
        abort(404, description="Student not found")

    student_list = []
    for student in students:
        student_list.append(student.to_dict())

    return jsonify(student_list), 200

@teach.route('/students/mark_list', methods=['PUT'])
@teacher_required
def add_student_assessment():
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    # token = request.headers['Authorization'].split(" ")[1]  # Bearer <token>
    # data = jwt.decode(token, os.getenv("TEACHER_JWT_SECRET"), algorithms=["HS256"])
    # teacher_id = data['teacher_id']

    for student in data:
        mark_list = storage._DBStorage__session.query(MarkList).filter_by(id=student['id']).first()
        if not mark_list:
            abort(404, description="Student not found")
        mark_list.score = student['score']
        storage.add(mark_list)

    return jsonify({"message": "Student Mark Updated Successfully!"}), 201

@teach.route('/dashboard', methods=['GET'])
@teacher_required
def teacher_dashboard():
    token = request.headers['Authorization'].split(" ")[1]  # Bearer <token>
    data = jwt.decode(token, os.getenv("TEACHER_JWT_SECRET"), algorithms=["HS256"])
    user_data = storage.get(Teacher, data['teacher_id'])
    return jsonify(user_data), 200
