import jwt
from datetime import datetime, timedelta
from flask import current_app  # Import current_app to access app context
from functools import wraps
from flask import request, jsonify
from models import storage
from models.student import Student
from models.teacher import Teacher
# from models.users import User
from models.admin import Admin


# Function to generate JWT for Admins
def create_admin_token(admin_id):
    payload = {
        'id': admin_id,
        'exp': datetime.utcnow() + timedelta(minutes=30),  # Admin token expires in 30 minutes
        'role': 'admin'
    }
    token = jwt.encode(payload, current_app.config["ADMIN_SECRET_KEY"], algorithm="HS256")
    return token

# Function to generate JWT for teachers
def create_teacher_token(teacher_id):
    payload = {
        'id': teacher_id,
        'exp': datetime.utcnow() + timedelta(minutes=15),  # teacher token expires in 15 minutes
        'role': 'teacher'
    }
    token = jwt.encode(payload, current_app.config["TEACHER_SECRET_KEY"], algorithm="HS256")
    return token

# Function to generate JWT for students
def create_student_token(student_id):
    payload = {
        'id': student_id,
        'exp': datetime.utcnow() + timedelta(minutes=15),  # teacher token expires in 15 minutes
        'role': 'student'
    }
    token = jwt.encode(payload, current_app.config["STUDENT_SECRET_KEY"], algorithm="HS256")
    return token

# Decorator for Admin JWT verification
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]  # Bearer token

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            payload = jwt.decode(token, current_app.config["ADMIN_SECRET_KEY"], algorithms=["HS256"])
            admin_data = storage.get_first(Admin, id=payload['id'])
            if not admin_data:
                return jsonify({'message': 'Admin not found!'}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Admin token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid Admin token'}), 401

        return f(admin_data, *args, **kwargs)

    return decorated_function


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
            payload = jwt.decode(token, current_app.config["TEACHER_SECRET_KEY"], algorithms=["HS256"])
            teacher_data = storage.get_first(Teacher, id=payload['id'])
            if not teacher_data:
                return jsonify({'message': 'Teacher not found!'}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Teacher token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid Teacher token'}), 401

        return f(teacher_data, *args, **kwargs)

    return decorated_function

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
            payload = jwt.decode(token, current_app.config["STUDENT_SECRET_KEY"], algorithms=["HS256"])
            student_data = storage.get_first(Student, id=payload['id'])
            if not student_data:
                return jsonify({'message': 'Student not found!'}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Student token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid Student token'}), 401

        return f(student_data, *args, **kwargs)

    return decorated_function
