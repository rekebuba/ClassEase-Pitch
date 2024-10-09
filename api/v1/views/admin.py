#!/usr/bin/python3

from flask import request, jsonify
from models import storage
from flask import Blueprint
from models.admin import Admin
from models.subject import Subject
from models.teacher import Teacher
from models.grade import Grade
from models.student import Student
from models.section import Section
from models.mark_list import MarkList
from models.assessment import Assessment
from models.average_result import AVRGResult
from sqlalchemy import update, select, and_
from urllib.parse import urlparse, parse_qs
from api.v1.views.utils import create_admin_token, admin_required


auth = Blueprint('auth', __name__, url_prefix='/api/v1/admin')


@auth.route('/registration', methods=['POST'])
def register_new_admin():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Not a JSON"}), 404

    user = Admin(name=data['name'], email=data['email'])
    user.hash_password(user.id)

    storage.add(user)
    return jsonify({"message": "Admin registered successfully!"}), 201


@auth.route('/login', methods=['POST'])
def admin_login():
    data = request.get_json()

    user = storage.get_first(Admin, email=data['email'])
    if user and user.check_password(data['password']):
        access_token = create_admin_token(user.id)
        return jsonify(access_token=access_token), 200

    return jsonify({"error": "Invalid credentials"}), 401


@auth.route('/dashboard', methods=['GET'])
@admin_required
def admin_dashboard(admin_data):
    return jsonify(admin_data.to_dict()), 200


def decode(subject: str, grade):
    code = subject[:3].upper() + str(grade)
    return code


# @auth.route('/student/courses', methods=['PUT'])
# @admin_required
# def update_course(admin_data):
#     data = request.get_json()
#     if not data:
#         return jsonify({"error": "Not a JSON"}), 404

#     grade = storage.get_first(Grade, grade=data['grade'])
#     if not grade:
#         return jsonify({"error": "No grade found for the student"}), 404

#     for course in data['subjects']:
#         code = decode(course, data['grade'])
#         subject = storage.get_first(Subject, code=code, grade_id=grade.id, name=course)
#         if not subject:
#             subject = Subject(name=course, code=code, grade_id=grade.id)
#             storage.add(subject)

#     return jsonify({"message": "Course updated successfully!"}), 201


@auth.route('/teacher/detail/course', methods=['PUT'])
@admin_required
def assign_course(admin_data):
    # Get the teacher by ID
    url = request.url
    parsed_url = urlparse(url)
    teacher_id = parse_qs(parsed_url.query)['teacher_id'][0]

    teacher = storage.get_first(Teacher, id=teacher_id)
    if not teacher:
        return jsonify({"error": "Teacher not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    # Get the grade_id from the Grade table
    grade_id = storage.get_session().execute(
        select(Grade.id).where(Grade.grade == data['grade'])
    ).scalars().first()
    if not grade_id:
        return jsonify({"error": "No grade found for the teacher"}), 404

    # Update the Subject table
    subject_update_result = storage.get_session().execute(
        update(Subject)
        .where(and_(
            Subject.grade_id == grade_id,
            Subject.name == data['subject'],
            Subject.school_year == data['school_year']
        ))
        .values(teacher_id=teacher.id)
    )

    if subject_update_result.rowcount == 0:
        return jsonify({"error": "Subject not found"}), 404

    # Update the Section table
    section_update_result = storage.get_session().execute(
        update(Section)
        .where(and_(
            Section.grade_id == grade_id,
            Section.school_year == data['school_year'],
            Section.section.in_(data['section'])
        ))
        .values(teacher_id=teacher.id)
    )

    if section_update_result.rowcount == 0:
        return jsonify({"error": "Section not found"}), 404

    # Commit the updates to the database
    storage.save()

    # Get section_id(s) based on the updated teacher_id
    section_result = storage.get_session().execute(
        select(Section.id).where(Section.teacher_id == teacher.id)
    ).scalars().all()  # Get all section IDs

    if not section_result:
        return jsonify({"error": "No sections found for the teacher"}), 404

    # Get subject_id(s) based on the updated teacher_id
    subject_result = storage.get_session().execute(
        select(Subject.id).where(Subject.teacher_id == teacher.id)
    ).scalars().all()

    if not subject_result:
        return jsonify({"error": "No subjects found for the teacher"}), 404

    # Update the MarkList table
    storage.get_session().execute(
        update(MarkList)
        .where(and_(
            MarkList.grade_id == grade_id,
            MarkList.section_id.in_(section_result),
            MarkList.subject_id.in_(subject_result),
            MarkList.school_year == data['school_year']
        ))
        .values(teacher_id=teacher.id)
    )

    # Commit the final updates to the database
    storage.save()

    return jsonify({"message": "Teacher assigned successfully!"}), 201


@auth.route('/teachers', methods=['GET'])
@admin_required
def all_teachers(admin_data):
    teachers = storage.all(Teacher)
    print(teachers)
    if not teachers:
        return jsonify({"error": "No teachers found"}), 404
    return jsonify([teacher.to_dict() for teacher in teachers]), 200


@auth.route('/students/mark_list', methods=['PUT'])
@admin_required
def create_mark_list(admin_data):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 404

    # Get the grade_id from the Grade table
    grade_id = storage.get_session().execute(
        select(Grade.id).where(Grade.grade == data['grade'])
    ).scalars().first()
    if not grade_id:
        return jsonify({"error": "Grade not found"}), 404

    # Update the Section table
    for sections in data['sections']:
        if not storage.get_first(Section, grade_id=grade_id, section=sections, school_year=data['school_year']):
            section = Section(grade_id=grade_id, section=sections,
                              school_year=data['school_year'])
            storage.add(section)

    students = (
        storage.get_session().query(Student)
        .filter(Student.grade_id == grade_id)
        .all()
    )

    # Assign a section randomly to students who do not have one
    for student in students:
        if not student.section_id:
            section = storage.get_random(Section, grade_id=grade_id)
            if not section:
                return jsonify({"error": "Section not found"}), 404
            storage.get_session().execute(
                update(Student)
                .where(Student.id == student.id)
                .values(section_id=section.id)
            )

    storage.save()

    # Update the Subject table
    for course in data['subjects']:
        # TODO: This is not a good way to generate a code
        code = decode(course, data['grade'])
        subject = storage.get_first(
            Subject, code=code, grade_id=grade_id, name=course)
        if not subject:
            subject = Subject(name=course, code=code, grade_id=grade_id, school_year=data['school_year'])
            storage.add(subject)

    """
    Wrapping the operations inside with ensures that all operations are treated as a single transaction.
    If an error occurs, none of the changes will be committed, which is good for data integrity.
    """
    with storage.get_session().begin():
        mark_lists = []  # A list to hold mark_list objects
        assessments = []  # A list to hold assessment objects
        average_result = []
        for student in students:
            subjects = storage.get_all(Subject, grade_id=grade_id)
            if not subjects:
                return jsonify({"error": "Subjects for the current grade not found"}), 404

            for subject in subjects:
                for assessment_type in data['assessment_type']:
                    values = {
                        "student_id": student.id,
                        "grade_id": grade_id,
                        "teacher_id": subject.teacher_id,
                        "section_id": student.section_id,
                        "subject_id": subject.id,
                        "semester": data['semester'],
                        "school_year": data['school_year'],
                    }
                    mark_lists.append(MarkList(**values, **assessment_type))
                assessments.append(Assessment(
                    student_id=student.id, subject_id=subject.id, semester=data['semester'], school_year=data['school_year']))
            average_result.append(AVRGResult(
                student_id=student.id, semester=data['semester'], school_year=data['school_year']))
        storage.get_session().bulk_save_objects(mark_lists)
        storage.get_session().bulk_save_objects(assessments)
        storage.get_session().bulk_save_objects(average_result)

    return jsonify({"message": "Mark list created successfully!"}), 201


@auth.route('/students/mark_list', methods=['GET'])
@admin_required
def show_mark_list(admin_data):
    url = request.url
    parsed_url = urlparse(url)
    data = parse_qs(parsed_url.query)

    grade = storage.get_first(Grade, grade=data['grade'][0])
    if not grade:
        return jsonify({"error": "Grade not found"}), 404

    section = storage.get_first(
        Section, grade_id=grade.id, section=data['section'][0], school_year=data['school_year'][0])
    if not section:
        return jsonify({"error": "Section not found"}), 404

    subject = storage.get_first(
        Subject, grade_id=grade.id, name=data['subject'][0])
    if not subject:
        return jsonify({"error": "Subject not found"}), 404

    students = storage.get_all(MarkList, grade_id=grade.id, section_id=section.id,
                               subject_id=subject.id, semester=data['semester'][0],
                               school_year=data['school_year'][0])
    if not students:
        return jsonify({"error": "Student not found"}), 404

    student_list = []
    for student in students:
        student_list.append(student.to_dict())

    return jsonify(student_list), 200
