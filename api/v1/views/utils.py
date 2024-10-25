import jwt
from datetime import datetime, timedelta
from flask import current_app  # Import current_app to access app context
from functools import wraps
from flask import request, jsonify
from models import storage
from models.student import Student
from models.stud_yearly_record import StudentYearlyRecord
from models.teacher import Teacher
from models.admin import Admin
from sqlalchemy import func
from models import storage
from models.mark_list import MarkList
from models.average_result import AVRGResult
from apscheduler.schedulers.background import BackgroundScheduler


# Function to generate JWT for Admins
def create_admin_token(admin_id):
    payload = {
        'id': admin_id,
        # Admin token expires in 30 minutes
        'exp': datetime.utcnow() + timedelta(minutes=30),
        'role': 'admin'
    }
    token = jwt.encode(
        payload, current_app.config["ADMIN_SECRET_KEY"], algorithm="HS256")
    return token


# Function to generate JWT for teachers
def create_teacher_token(teacher_id):
    payload = {
        'id': teacher_id,
        # teacher token expires in 15 minutes
        'exp': datetime.utcnow() + timedelta(minutes=15),
        'role': 'teacher'
    }
    token = jwt.encode(
        payload, current_app.config["TEACHER_SECRET_KEY"], algorithm="HS256")
    return token


# Function to generate JWT for students
def create_student_token(student_id):
    payload = {
        'id': student_id,
        # teacher token expires in 15 minutes
        'exp': datetime.utcnow() + timedelta(minutes=15),
        'role': 'student'
    }
    token = jwt.encode(
        payload, current_app.config["STUDENT_SECRET_KEY"], algorithm="HS256")
    return token


# Decorator for Admin JWT verification
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]  # Bearer token

        if not token:
            return jsonify({"error": "Unauthorized", "reason": "UNAUTHORIZED"}), 401

        try:
            payload = jwt.decode(
                token, current_app.config["ADMIN_SECRET_KEY"], algorithms=["HS256"])
            admin_data = storage.get_first(Admin, id=payload['id'])
            if not admin_data:
                return jsonify({"error": "Unauthorized", "reason": "UNAUTHORIZED"}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Unauthorized", "reason": "SESSION_EXPIRED"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Unauthorized", "reason": "UNAUTHORIZED"}), 401

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
            payload = jwt.decode(
                token, current_app.config["TEACHER_SECRET_KEY"], algorithms=["HS256"])
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
            payload = jwt.decode(
                token, current_app.config["STUDENT_SECRET_KEY"], algorithms=["HS256"])
            student_data = storage.get_first(
                StudentYearlyRecord, student_id=payload['id'])
            if not student_data:
                print("notfound")
                return jsonify({'message': 'Student not found!'}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Student token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid Student token'}), 401

        return f(student_data, *args, **kwargs)

    return decorated_function


def update_overall_averages():
    averages = storage.get_session().query(
        MarkList.subject_id,
        func.sum(MarkList.score).label('total_score')
    ).group_by(MarkList.subject_id).all()

    for avg in averages:
        overall = storage.get_session().query(AVRGResult).filter_by(
            student_id=avg.student_id
        ).first()

        if not overall:
            # overall = AVRGResult(
            #     student_id=avg.student_id,
            #     average_score=avg.average_score
            # )
            # storage.add(overall)
            return
        else:
            overall.average = avg.average_score

    storage.save()

# # Initialize the scheduler
# scheduler = BackgroundScheduler()
# scheduler.add_job(update_overall_averages, 'interval', hours=1)
# scheduler.start()
