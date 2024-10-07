#!/usr/bin/python3

from flask import request, jsonify, abort
from models import storage
from models.users import User
from api.v1.views import app_views, auth
from models.subject import Subject
from models.teacher import Teacher
from models.grade import Grade
from models.student import Student
from models.section import Section
from models.mark_list import MarkList
from models.assessment import Assessment
from functools import wraps
from sqlalchemy import update, select, and_
from sqlalchemy.sql.expression import func
from urllib.parse import urlparse, parse_qs
import random
import jwt
import os


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
            data = jwt.decode(token, os.getenv(
                "ADMIN_JWT_SECRET"), algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Admin token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid Admin token'}), 401

        return f(*args, **kwargs)

    return decorated_function


@auth.route('/register', methods=['POST'])
def admin_register():
    data = request.get_json()

    if not data:
        abort(400, description="Not a JSON")

    user = User(name=data['name'], email=data['email'])
    user.hash_password(data['password'])

    storage.add(user)
    return jsonify({"message": "Admin registered successfully!"}), 201


@auth.route('/dashboard', methods=['GET'])
@admin_required
def admin_dashboard():
    token = request.headers['Authorization'].split(" ")[1]  # Bearer <token>
    data = jwt.decode(token, os.getenv(
        "ADMIN_JWT_SECRET"), algorithms=["HS256"])
    user_data = storage.get(User, data['admin_id'])
    return jsonify(user_data), 200


def decode(subject: str, grade):
    code = subject[:3].upper() + str(grade)
    return code


@auth.route('/student/courses', methods=['PUT'])
@admin_required
def update_course():
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    grade = storage._DBStorage__session.query(
        Grade).filter_by(grade=data['grade']).first()

    if not grade:
        grade = Grade(grade=data['grade'])
        storage.add(grade)

    for course in data['subjects']:
        code = decode(course, data['grade'])
        subject = storage._DBStorage__session.query(
            Subject).filter_by(code=code).first()
        if not subject:
            subject = Subject(name=course, code=code, grade_id=grade.id)
            storage.add(subject)

    return jsonify({"message": "Course updated successfully!"}), 201


@auth.route('/teacher/<id>/detail/course', methods=['PUT'])
@admin_required
def assign_course(id):
    # Get the teacher by ID
    teacher = storage._DBStorage__session.query(
        Teacher).filter_by(id=id).first()
    if not teacher:
        abort(404, description="Teacher not found")

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    # Get the grade_id from the Grade table
    grade_id = storage._DBStorage__session.execute(
        select(Grade.id).where(Grade.grade == data['grade'])
    ).scalars().first()
    if not grade_id:
        abort(404, description="Grade not found")

    # Update the Subject table
    storage._DBStorage__session.execute(
        update(Subject)
        .where(and_(
            Subject.grade_id == grade_id,
            Subject.name == data['subject']
        ))
        .values(teacher_id=teacher.id)
    )

    # Update the Section table
    storage._DBStorage__session.execute(
        update(Section)
        .where(and_(
            Section.grade_id == grade_id,
            Section.section.in_(data['section'])
        ))
        .values(teacher_id=teacher.id)
    )

    # Commit the updates to the database
    storage.save()

    # Get section_id(s) based on the updated teacher_id
    section_result = storage._DBStorage__session.execute(
        select(Section.id).where(Section.teacher_id == teacher.id)
    ).scalars().all()  # Get all section IDs

    if not section_result:
        abort(404, description="No sections found for the teacher")

    # Get subject_id(s) based on the updated teacher_id
    subject_result = storage._DBStorage__session.execute(
        select(Subject.id).where(Subject.teacher_id == teacher.id)
    ).scalars().all()

    if not subject_result:
        abort(404, description="No subjects found for the teacher")

    # Update the MarkList table
    storage._DBStorage__session.execute(
        update(MarkList)
        .where(and_(
            MarkList.grade_id == grade_id,
            MarkList.section_id.in_(section_result),
            MarkList.subject_id.in_(subject_result)
        ))
        .values(teacher_id=teacher.id)
    )

    # Commit the final updates to the database
    storage.save()

    return jsonify({"message": "Teacher assigned successfully!"}), 201


@auth.route('/teachers', methods=['GET'])
def all_teachers():
    teachers = storage.all(Teacher)
    return jsonify([teacher.to_dict() for teacher in teachers]), 200


@auth.route('/students/mark_list', methods=['PUT'])
@admin_required
def create_mark_list():
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    # Get the grade_id from the Grade table
    grade_id = storage._DBStorage__session.execute(
        select(Grade.id).where(Grade.grade == data['grade'])
    ).scalars().first()
    if not grade_id:
        abort(404, description="Grade not found")

    for sections in data['sections']:
        if not storage._DBStorage__session.query(Section).filter_by(grade_id=grade_id, section=sections).first():
            section = Section(grade_id=grade_id, section=sections)
            storage.add(section)

    students = (
        storage._DBStorage__session.query(Student)
        .filter(Student.grade_id == grade_id)
        .all()
    )
    

    for student in students:
        section = storage._DBStorage__session.query(Section).filter_by(
            grade_id=grade_id).order_by(func.rand()).first()
        if not section:
            abort(404, description="Section not found")
        storage._DBStorage__session.execute(
            update(Student)
            .where(Student.id == student.id)
            .values(section_id=section.id)
        )
    storage.save()

    """
    Wrapping the operations inside with ensures that all operations are treated as a single transaction.
    If an error occurs, none of the changes will be committed, which is good for data integrity.
    """
    with storage._DBStorage__session.begin():
        mark_lists = []  # A list to hold mark_list objects
        assessments = []  # A list to hold assessment objects
        for student in students:
            subjects = storage._DBStorage__session.query(Subject).filter_by(grade_id=grade_id).all()
            for subject in subjects:
                for assessment_type in data['assessment_type']:
                    values = {
                        "student_id": student.id,
                        "grade_id": grade_id,
                        "teacher_id": subject.teacher_id,
                        "section_id": student.section_id,
                        "subject_id": subject.id
                    }
                    mark_lists.append(MarkList(**values, **assessment_type))
                    assessments.append(Assessment(student_id=student.id, subject_id=subject.id))
        storage._DBStorage__session.bulk_save_objects(mark_lists)
        storage._DBStorage__session.bulk_save_objects(assessments)

    return jsonify({"message": "Mark List Created successfully!"}), 201

@auth.route('/students/mark_list', methods=['GET'])
@admin_required
def show_mark_list():
    url = request.url
    parsed_url = urlparse(url)
    data = parse_qs(parsed_url.query)

    grade = storage._DBStorage__session.query(Grade).filter_by(grade=data['grade']).first()
    if not grade:
        abort(404, description="Grade not found")

    section = storage._DBStorage__session.query(Section).filter_by(grade_id=grade.id, section=data['section']).first()
    if not section:
            abort(404, description="Section not found")

    subject = storage._DBStorage__session.query(Subject).filter_by(grade_id=grade.id, name=data['subject']).first()
    if not subject:
        abort(404, description="Subject not found")

    students = storage._DBStorage__session.query(MarkList).filter_by(grade_id=grade.id, section_id=section.id, subject_id=subject.id).all()
    if not students:
        abort(404, description="Student not found")

    student_list = []
    for student in students:
        student_list.append(student.to_dict())

    return jsonify(student_list), 200
