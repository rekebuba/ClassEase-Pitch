from flask import request, jsonify, abort
from models import storage
from models.users import User
from models.grade import Grade
from models.student import Student
from models.section import Section
from api.v1.views import app_views, stud
from functools import wraps
import jwt
import os

# Decorator for student JWT verification
def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]  # Bearer token

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, os.getenv("STUDENT_JWT_SECRET"), algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Student token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid Student token'}), 401

        return f(*args, **kwargs)

    return decorated_function

@app_views.route('/student/registration', methods=['POST'])
def register_new_student():
    data = request.get_json()

    if not data:
        abort(400, description="Not a JSON")

    grade = storage._DBStorage__session.query(Grade).filter_by(grade=data['grade']).first()
    if not grade:
        grade = Grade(grade=data['grade'])
        storage.add(grade)

    students = Student(**data, grade_id=grade.id)
    students.hash_password(students.id)
    storage.add(students)

    return  jsonify({"message": "Student registered successfully!"}), 201


@stud.route('/dashboard', methods=['GET'])
@student_required
def student_dashboard():
    token = request.headers['Authorization'].split(" ")[1]  # Bearer <token>
    data = jwt.decode(token, os.getenv("STUDENT_JWT_SECRET"), algorithms=["HS256"])
    user_data = storage.get(Student, data['student_id'])
    return jsonify(user_data), 200
