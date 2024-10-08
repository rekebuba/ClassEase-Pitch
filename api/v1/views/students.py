from flask import request, jsonify, abort
from models import storage
# from models.users import User
from models.grade import Grade
from models.student import Student
from models.section import Section
from functools import wraps
import jwt
import os
from flask import Blueprint
from api.v1.views.utils import create_student_token, student_required


stud = Blueprint('stud', __name__, url_prefix='/api/v1/student')


@stud.route('/registration', methods=['POST'])
def register_new_student():
    data = request.get_json()

    if not data:
        abort(400, description="Not a JSON")

    grade = storage.get_first(Grade, grade=data['grade'])
    if not grade:
        grade = Grade(grade=data['grade'])
        storage.add(grade)

    students = Student(**data, grade_id=grade.id)
    students.hash_password(students.id)
    storage.add(students)

    return  jsonify({"message": "Student registered successfully!"}), 201


@stud.route('/login', methods=['POST'])
def student_login():
    data = request.get_json()

    user = storage.get_first(Student, id=data['id'])
    if user and user.check_password(data['password']):
        access_token = create_student_token(user.id)
        return jsonify(access_token=access_token), 200

    return jsonify({"error": "Invalid credentials"}), 401

@stud.route('/dashboard', methods=['GET'])
@student_required
def student_dashboard(student_data):
    return jsonify(student_data.to_dict()), 200
