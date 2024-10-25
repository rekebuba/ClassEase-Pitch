#!/usr/bin/python3

from flask import request, jsonify
from models import storage
from flask import Blueprint
from models.users import User
from models.admin import Admin
from models.subject import Subject
from models.teacher import Teacher
from models.grade import Grade
from models.student import Student
from models.section import Section
from models.mark_list import MarkList
from models.assessment import Assessment
from models.average_result import AVRGResult
from models.stud_yearly_record import StudentYearlyRecord
from models.teacher_record import TeachersRecord
from sqlalchemy import update, select, and_
from urllib.parse import urlparse, parse_qs
from api.v1.views.utils import create_admin_token, admin_required
from math import ceil


auth = Blueprint('auth', __name__, url_prefix='/api/v1/admin')


@auth.route('/registration', methods=['POST'])
def register_new_admin():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Not a JSON"}), 404

    # Check if required fields are present
    if 'name' not in data or 'email' not in data:
        return jsonify({"error": "Missing name or email"}), 400

    new_admin = User(role='Admin')
    new_admin.hash_password(new_admin.id)

    try:
        # Save User first
        storage.add(new_admin)

        # Create the Admin object, using the same id
        admin = Admin(id=new_admin.id, name=data['name'], email=data['email'])

        # Save Admin
        storage.add(admin)
    except Exception as e:
        storage.rollback()
        print(e)
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Admin registered successfully!"}), 201


@auth.route('/teachers/registration', methods=['POST'])
# @admin_required
def register_new_teacher():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Not a JSON"}), 404

    required_data = {
        "first_name",
        "last_name",
        "age",
        "gender",
        "email",
        "phone",
        "address",
        "experience",
        "qualification",
        "subject_taught",
    }

    # Check if required fields are present
    for field in required_data:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400

    # check if a Teacher with the same email, first name, and last name already exists
    existing_teacher = storage.get_first(
        Teacher,
        email=data['email'],
        first_name=data['first_name'],
        last_name=data['last_name']
    )
    if existing_teacher:
        return jsonify({"error": "Teacher already exists"}), 409

    new_teacher = User(role='Teacher')
    new_teacher.hash_password(new_teacher.id)

    try:
        # Save User first
        storage.add(new_teacher)

        # Create the Teacher object, using the same id
        teacher = Teacher(id=new_teacher.id, **data)

        # Save the Teacher object
        storage.add(teacher)
    except Exception as e:
        storage.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Teacher registered successfully!"}), 201


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


@auth.route('/assign-teacher', methods=['PUT'])
@admin_required
def assign_class(admin_data):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    required_data = [
        'teacher_id',
        'grade',
        'section',
        'subjects_taught',
        'mark_list_year'
    ]
    # Check if required fields are present
    for field in required_data:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400

    # Get the teacher by ID
    teacher = storage.get_first(Teacher, id=data['teacher_id'])
    if not teacher:
        return jsonify({"error": "Teacher not found"}), 404

    # Get the grade_id from the Grade table
    grade_id = storage.get_session().execute(
        select(Grade.id).where(Grade.grade == data['grade'])
    ).scalars().first()
    if not grade_id:
        return jsonify({"error": "No grade found for the teacher"}), 404

    # get the subject_id
    subjects_taught = storage.get_session().query(Subject).filter(
        Subject.grade_id == grade_id,
        Subject.name.in_(data['subjects_taught'])
    ).all()
    if not subjects_taught:
        return jsonify({"error": "Subject not found"}), 404

    try:
        for subject in subjects_taught:
            # get the section_id
            section_ids = [id[0] for id in storage.get_session().query(Section.id).filter(
                Section.grade_id == grade_id,
                Section.section.in_(data['section'])
            ).all()]

            if not section_ids:
                return jsonify({"error": f"Section not found, Mark List was not created for the grade {data['grade']}"}), 404

            for section_id in section_ids:
                # check if the teacher is already assigned to the subject
                teacher_record = storage.get_first(
                    TeachersRecord, teacher_id=teacher.id, grade_id=grade_id, section_id=section_id, subject_id=subject.id)
                if not teacher_record:
                    # update the teacher record
                    teacher_record = TeachersRecord(
                        teacher_id=teacher.id,
                        grade_id=grade_id,
                        section_id=section_id,
                        subject_id=subject.id
                    )

                    storage.add(teacher_record)

                # Update the MarkList table
                print(teacher_record.id)
                update_result = storage.get_session().execute(
                    update(MarkList)
                    .where(and_(
                        MarkList.grade_id == grade_id,
                        MarkList.section_id == section_id,
                        MarkList.subject_id == subject.id,
                        MarkList.year == data['mark_list_year']
                    ))
                    .values(teachers_record_id=teacher_record.id)
                )

                # Commit the final updates to the database
                storage.save()
    except Exception as e:
        storage.rollback()
        print(str(e))
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Teacher assigned successfully!"}), 201


@auth.route('/students/mark_list', methods=['PUT'])
@admin_required
def create_mark_list(admin_data):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 404

    required_data = {
        'grade',
        'sections',
        'subjects',
        'assessment_type',
        'semester',
        'year'
    }

    # Check if required fields are present
    for field in required_data:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400
        elif field in {'grade', 'section', 'semester'} and type(data[field]) != int:
            return jsonify({"error": f"{field} must be an integer"}), 400
        elif field == 'assessment_type':
            for assessment in data[field]:
                if assessment.keys() != {'type', 'percentage'}:
                    return jsonify({"error": "Missing type or percentage"}), 400
                elif type(assessment['type']) != str or type(assessment['percentage']) != int:
                    return jsonify({"error": "Type must be a string and percentage must be an integer"}), 400

    # Get the grade_id from the Grade table
    grade_id = storage.get_session().execute(
        select(Grade.id).where(Grade.grade == data['grade'])
    ).scalars().first()
    if not grade_id:
        return jsonify({"error": "Grade not found"}), 404

    # Update the Section table
    existing_sections = {}
    for section in data['sections']:
        exists = storage.get_first(
            Section, grade_id=grade_id, section=section)
        if exists and storage.get_first(MarkList, section_id=exists.id, year=data['year']):
            existing_sections[section] = exists.id
        elif not exists:
            section = Section(grade_id=grade_id, section=section)
            storage.add(section)

    mark_list_exists = (
        storage.get_session().query(MarkList)
        .filter(MarkList.grade_id == grade_id,
                MarkList.semester == data['semester'],
                MarkList.year == data['year'],
                MarkList.section_id.in_(list(existing_sections.values())))
        .all()
    )

    if mark_list_exists:
        return jsonify({
            "error": f"Mark list already exists for grade = {data['grade']}, "
            f"Section = {' and '.join(map(str, list(existing_sections.keys())))}, "
            f"Semester = {data['semester']}, "
            f"School Year = {data['year']}"
        }), 400

    try:
        students = (
            storage.get_session().query(StudentYearlyRecord)
            .filter(StudentYearlyRecord.grade_id == grade_id, StudentYearlyRecord.year == data['year'])
            .all()
        )

        if not students:
            return jsonify({"error": f"No students found for the year {data['year']}"}), 404

        # Assign a section randomly to students who do not have one
        for student in students:
            if not student.section_id:
                section = storage.get_random(Section, grade_id=grade_id)
                if not section:
                    return jsonify({"error": "Section not found"}), 404
                update_result = storage.get_session().execute(
                    update(StudentYearlyRecord)
                    .where(StudentYearlyRecord.student_id == student.student_id)
                    .values(section_id=section.id)
                )

                if update_result.rowcount == 0:
                    return jsonify({"error": f"Failed to update section for student {student.student_id}"}), 500

        storage.save()

        # Update the Subject table
        for course in data['subjects']:
            # TODO:
            code = decode(course, data['grade'])
            subject = storage.get_first(
                Subject, code=code, grade_id=grade_id, name=course)
            if not subject:
                subject = Subject(name=course, code=code,
                                  grade_id=grade_id, year=data['year'])
                storage.add(subject)

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
                        "student_id": student.student_id,
                        "grade_id": grade_id,
                        "section_id": student.section_id,
                        "subject_id": subject.id,
                        "semester": data['semester'],
                        "year": data['year'],
                    }
                    mark_lists.append(MarkList(**values, **assessment_type))
                assessments.append(Assessment(
                    student_id=student.student_id, grade_id=grade_id, subject_id=subject.id, semester=data['semester'], year=data['year']))

            average_result.append(AVRGResult(
                student_id=student.student_id, semester=data['semester'], year=data['year']))

        # Save the objects to the database
        storage.get_session().bulk_save_objects(mark_lists)
        storage.get_session().bulk_save_objects(assessments)
        storage.get_session().bulk_save_objects(average_result)

        storage.save()
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Mark list created successfully!"}), 201


@auth.route('/students/mark_list', methods=['GET'])
@admin_required
def show_mark_list(admin_data):
    url = request.url
    parsed_url = urlparse(url)
    data = parse_qs(parsed_url.query)

    required_data = [
        'grade',
        'sections',
        'subject',
        'assessment_type',
        'semester',
        'year'
    ]
    # Check if required fields are present
    for field in required_data:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400

    grade = storage.get_first(Grade, grade=data['grade'][0])
    if not grade:
        return jsonify({"error": "Grade not found"}), 404

    section = storage.get_first(
        Section, grade_id=grade.id, section=data['section'][0], year=data['year'][0])
    if not section:
        return jsonify({"error": "Section not found"}), 404

    subject = storage.get_first(
        Subject, grade_id=grade.id, name=data['subject'][0])
    if not subject:
        return jsonify({"error": "Subject not found"}), 404

    students = storage.get_all(MarkList, grade_id=grade.id, section_id=section.id,
                               subject_id=subject.id, semester=data['semester'][0],
                               year=data['year'][0])
    if not students:
        return jsonify({"error": "Student not found"}), 404

    student_list = []
    for student in students:
        student_list.append(student.to_dict())

    return jsonify(student_list), 200


def paginate_query(query, page, limit):
    """
    Paginate SQLAlchemy queries.

    :param query: SQLAlchemy query object to paginate
    :param request: Flask request object to get query parameters (page, limit)
    :param default_limit: Default number of records per page if limit is not provided
    :return: Dictionary with paginated data and meta information
    """

    # Calculate total number of records
    total_items = query.count()

    # Calculate offset and apply limit and offset to the query
    offset = (page - 1) * limit
    paginated_query = query.limit(limit).offset(offset)

    # Get the paginated results
    items = paginated_query.all()

    # Calculate total pages
    total_pages = ceil(total_items / limit)

    # Return the paginated data and meta information
    return {
        "items": items,
        "meta": {
            "total_items": total_items,
            "current_page": page,
            "limit": limit,
            "total_pages": total_pages,
        }
    }


@auth.route('/manage/students', methods=['GET'])
@admin_required
def admin_student_data(admin_data):
    url = request.url
    parsed_url = urlparse(url)
    data = parse_qs(parsed_url.query)

    required_data = {
        'grade',
        'year'
    }

    # Check if required fields are present
    for field in required_data:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400

    grade = storage.get_first(Grade, grade=data['grade'][0])
    if not grade:
        return jsonify({"error": "Grade not found"}), 404
    print(data['year'][0])

    # Pagination and filtering params
    page = int(data['page'][0]) if 'page' in data else 1
    limit = int(data['limit'][0]) if 'limit' in data else 10
    search_term = data['search'][0] if 'search' in data else None

    query = storage.get_session().query(StudentYearlyRecord).filter(
        StudentYearlyRecord.grade_id == grade.id,
        StudentYearlyRecord.year == data['year'][0]
    )

    if search_term:
        search_pattern = f"%{search_term}%"
        joined = query.join(Student, Student.id ==
                            StudentYearlyRecord.student_id)
        query = joined.filter(
            Student.name.ilike(search_pattern) |
            StudentYearlyRecord.student_id.ilike(search_pattern)
        )

    # Use the paginate_query function to handle pagination
    paginated_result = paginate_query(query, page, limit)

    # Check if any students are found
    if not paginated_result['items']:
        return jsonify({"error": "No student found"}), 404

    student_list = []
    for student in paginated_result['items']:
        section = None
        student_data = storage.get_first(Student, id=student.student_id)
        if student.section_id:
            section = storage.get_first(Section, id=student.section_id).section
        if not student_data:
            return jsonify({"error": "No student found"}), 404

        student_mark = storage.get_all(
            MarkList, student_id=student_data.id, year=data['year'][0])

        if not student_mark:
            return jsonify({"error": f"Grade {data['grade'][0]} for the year {data['year'][0]} Dose not have mark list"}), 404

        # Filter Unique subjects for a student
        # Subquery to get unique subject_ids
        unique_subjects = (
            storage.get_session()
            .query(Assessment.subject_id)
            .filter(Assessment.student_id == student_data.id, Assessment.year == data['year'][0])
            .distinct()
            .all()
        )
        if not unique_subjects:
            return jsonify({"error": f"{student_data.name} does not have a mark list"}), 404

        performance = []
        for subject_id in unique_subjects:
            subject = storage.get_first(Subject, id=subject_id[0])
            semesters = {}
            for semester in storage.get_all(
                MarkList,
                student_id=student_data.id,
                subject_id=subject.id,
                year=data['year'][0]
            ):
                if semester.semester not in semesters:
                    semesters[semester.semester] = []
                semesters[semester.semester].append({
                    "type": semester.type,
                    "score": semester.score,
                    "percentage": semester.percentage
                })
            semester_result = {
                "subject": subject.name,
                "semesters": semesters
            }
            performance.append(semester_result)

        # Student Summary
        student_summary = {
            "student_id": student_data.id,
            "name": student_data.name,
            "father_name": student_data.father_name,
            "grand_father_name": student_data.grand_father_name,
            "grade": data['grade'][0],
            "section": section,
            "performance": performance,
            "year": student.year
        }

        student_list.append(student_summary)

    return jsonify({
        "students": student_list,
        "meta": paginated_result['meta']
    }
    ), 200


@auth.route('/teachers', methods=['GET'])
@admin_required
def all_teachers(admin_data):
    url = request.url
    parsed_url = urlparse(url)
    data = parse_qs(parsed_url.query)

    teachers = storage.get_session().query(Teacher)

    if not teachers:
        return jsonify({"error": "No teachers found"}), 404

    # Pagination and filtering params
    page = int(data['page'][0]) if 'page' in data else 1
    limit = int(data['limit'][0]) if 'limit' in data else 10
    search_term = data['search'][0] if 'search' in data else None

    # Use the paginate_query function to handle pagination
    paginated_result = paginate_query(teachers, page, limit)

    # Check if any Teachers are found
    if not paginated_result['items']:
        return jsonify({"error": "No Teacher found"}), 404

    teacher_list = []
    for teacher in paginated_result['items']:
        class_handled = []
        teachers_record = storage.get_all(
            TeachersRecord, teacher_id=teacher.id)
        for record in teachers_record:
            grade = storage.get_first(Grade, id=record.grade_id).grade
            section = storage.get_first(Section, id=record.section_id).section
            subject = storage.get_first(Subject, id=record.subject_id).name
            class_handled.append({
                "grade": grade,
                "section": section,
                "subject": subject
            })
            # Teacher Summary
        teacher_summary = {
            "id": teacher.id,
            "name": "Mr." + teacher.first_name + " " + teacher.last_name,
            "first_name": teacher.first_name,
            "last_name": teacher.last_name,
            "email": teacher.email,
            "phone": teacher.phone,
            "age": teacher.age,
            "experience": teacher.experience,
            "no_of_mark_list": teacher.no_of_mark_list,
            "record": class_handled,
            "subjects": [teacher.subject_taught],
            "qualifications": [teacher.qualification],
        }

        teacher_list.append(teacher_summary)

    return jsonify({
        "teachers": teacher_list,
        "meta": paginated_result['meta']
    }), 200
