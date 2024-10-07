#!/usr/bin/python3
from models import storage
from api.v1.views import app_views, auth, teach, stud
from models.users import User
from models.teacher import Teacher
from models.student import Student
from flask import Flask, jsonify, request, abort, make_response
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import jwt


# Load environment variables from .env file
load_dotenv()

# create an instance of the Flask class
app = Flask(__name__)
app.config["ADMIN_SECRET_KEY"] = os.getenv("ADMIN_JWT_SECRET")
app.config["TEACHER_SECRET_KEY"] = os.getenv("TEACHER_JWT_SECRET")
app.config["STUDENT_SECRET_KEY"] = os.getenv("STUDENT_JWT_SECRET")


# Function to generate JWT for Admins
def create_admin_token(admin_id):
    payload = {
        'admin_id': admin_id,
        'exp': datetime.utcnow() + timedelta(minutes=30),  # Admin token expires in 30 minutes
        'role': 'admin'
    }
    token = jwt.encode(payload, app.config["ADMIN_SECRET_KEY"], algorithm="HS256")
    return token

# Function to generate JWT for teachers
def create_teacher_token(teacher_id):
    payload = {
        'teacher_id': teacher_id,
        'exp': datetime.utcnow() + timedelta(minutes=15),  # teacher token expires in 15 minutes
        'role': 'teacher'
    }
    token = jwt.encode(payload, app.config["TEACHER_SECRET_KEY"], algorithm="HS256")
    return token

# Function to generate JWT for students
def create_student_token(student_id):
    payload = {
        'student_id': student_id,
        'exp': datetime.utcnow() + timedelta(minutes=15),  # teacher token expires in 15 minutes
        'role': 'student'
    }
    token = jwt.encode(payload, app.config["STUDENT_SECRET_KEY"], algorithm="HS256")
    return token

@auth.route('/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    user = storage._DBStorage__session.query(User).filter_by(email=data['email']).first()

    if user and user.check_password(data['password']):
        access_token = create_admin_token(user.id)
        return jsonify(access_token=access_token), 200

    return jsonify({"error": "Invalid credentials"}), 401

@teach.route('/login', methods=['POST'])
def teacher_login():
    data = request.get_json()
    user = storage._DBStorage__session.query(Teacher).filter_by(email=data['email']).first()

    if user and user.check_password(data['password']):
        access_token = create_teacher_token(user.id)
        return jsonify(access_token=access_token), 200

    return jsonify({"error": "Invalid credentials"}), 401


@stud.route('/login', methods=['POST'])
def student_login():
    data = request.get_json()
    user = storage._DBStorage__session.query(Student).filter_by(id=data['id']).first()

    if user and user.check_password(data['password']):
        access_token = create_student_token(user.id)
        return jsonify(access_token=access_token), 200

    return jsonify({"error": "Invalid credentials"}), 401



app.register_blueprint(stud)
app.register_blueprint(auth)
app.register_blueprint(teach)
app.register_blueprint(app_views)


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    app.run(host=host, port=port, debug=True) 
