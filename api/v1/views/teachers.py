#!/usr/bin/python3
"""Teacher views module for the API"""

from flask import request, jsonify
from sqlalchemy import func
from models import storage
from datetime import datetime
from models.users import User
from models.grade import Grade
from models.student import Student
from models.section import Section
from models.subject import Subject
from models.assessment import Assessment
from models.mark_list import MarkList
from models.average_result import AVRGResult
from models.teacher import Teacher
from models.teacher_record import TeachersRecord
from models.stud_yearly_record import StudentYearlyRecord
from urllib.parse import urlparse, parse_qs
from sqlalchemy import update, and_
from flask import Blueprint
from api.v1.views.utils import teacher_required
from api.v1.views.methods import paginate_query
from models.base_model import BaseModel


teach = Blueprint('teach', __name__, url_prefix='/api/v1/teacher')


@teach.route('/dashboard', methods=['GET'])
@teacher_required
def teacher_dashboard(teacher_data):
    """
    Handle the teacher dashboard view.

    Args:
        teacher_data (object): The teacher data object. Should have a `to_dict` method.

    Returns:
        Response: A JSON response containing the teacher data if found,
                  otherwise an error message with a 404 status code.
    """
    if not teacher_data:
        return jsonify({"error": "Teacher not found"}), 404
    return jsonify(teacher_data.to_dict()), 200


@teach.route('/update-profile', methods=['PUT'])
@teacher_required
def update_teacher_profile(teacher_data):
    """
    Update the profile of a teacher.

    This function updates the profile information of a teacher based on the provided JSON data.
    It requires the fields 'first_name', 'email', and 'phone' to be present in the request data.
    Optionally, it can also update the teacher's password if 'new_password' and 'current_password' are provided.

    Args:
        teacher_data (object): The teacher object whose profile is to be updated.

    Returns:
        Response: A JSON response indicating the result of the update operation.
            - 200: Profile updated successfully.
            - 400: If the request data is not JSON, or if required fields are missing, or if the current password is incorrect.
            - 404: If the user is not found.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    required_data = {
        'first_name',
        'email',
        'phone',
    }

    for field in required_data:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400

    teacher_data.first_name = data['first_name']
    teacher_data.email = data['email']
    teacher_data.phone = data['phone']

    if 'new_password' in data:
        if 'current_password' not in data:
            return jsonify({"error": "Missing old password"}), 400
        user = storage.get_first(User, id=teacher_data.id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        if not user.check_password(data['current_password']):
            return jsonify({"error": "Incorrect password"}), 400

        user.hash_password(data['new_password'])
    storage.save()

    return jsonify({"message": "Profile Updated Successfully"}), 200


@teach.route('/students/mark_list', methods=['GET'])
@teacher_required
def get_list_of_students(teacher_data):
    """
    Retrieves a list of students based on the provided teacher data and query parameters.

    Args:
        teacher_data (object): The teacher data object containing the teacher's information.

    Returns:
        Response: A JSON response containing the list of students and relevant header information,
                  or an error message with the appropriate HTTP status code.

    Query Parameters:
        grade (str): The grade to filter students by.
        sections (str): Comma-separated list of sections to filter students by.
        semester (str): The semester to filter students by.
        year (str): The year to filter students by.

    Response JSON Structure

    Error Responses:
        400: {"error": "Bad Request"} - If required query parameters are missing.
        400: {"error": "Missing <field>"} - If a specific required field is missing.
        404: {"error": "Grade not found"} - If the specified grade does not exist.
        404: {"error": "Section not found"} - If the specified section does not exist.
    """
    url = request.url
    parsed_url = urlparse(url)
    data = parse_qs(parsed_url.query)

    if not data:
        return jsonify({"error": "Bad Request"}), 400

    required_data = {
        'subject_id',
        'grade',
        'sections',
        'semester',
        'year'
    }

    for field in required_data:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400

    grade = storage.get_first(Grade, grade=data['grade'][0])
    if not grade:
        return jsonify({"error": "Grade not found"}), 404

    # get the section_id
    section = storage.get_first(Section,
                                    grade_id=grade.id,
                                    section=(data['sections'][0]))
    if not section:
        return jsonify({"error": "Section not found"}), 404

    # Pagination and filtering params
    page = int(data['page'][0]) if 'page' in data else 1
    limit = int(data['limit'][0]) if 'limit' in data else 10
    search_term = data['search'][0] if 'search' in data else None

    query = (
        storage.get_session()
        .query(Student.id,
               Student.name,
               Student.father_name,
               Student.grand_father_name,
               Section.section,
               AVRGResult.section_id,
               AVRGResult.grade_id,
               Assessment.subject_id,
               Assessment.total,
               Assessment.rank,
               Assessment.semester,
               Assessment.year
               )  # Explicitly specify the table being queried
        .select_from(Assessment)
        .join(TeachersRecord, TeachersRecord.id == Assessment.teachers_record_id)
        .join(AVRGResult, AVRGResult.student_id == Assessment.student_id)
        .join(Student, Student.id == Assessment.student_id)
        .join(Section, Section.id == AVRGResult.section_id)
        .filter(
            and_(
                TeachersRecord.teacher_id == teacher_data.id,
                Assessment.subject_id == data['subject_id'][0],
                AVRGResult.section_id == section.id
            )
        )
        .order_by(Section.section.asc(), Student.name.asc(), Student.father_name.asc(), Student.grand_father_name.asc(), Student.id.asc())
    )

    if search_term:
        search_pattern = f"%{search_term}%"
        query = (
            query.filter(Student.id.ilike(search_pattern) |
                         Student.name.ilike(search_pattern) |
                         Student.father_name.ilike(search_pattern) |
                         Student.grand_father_name.ilike(search_pattern)
                         )
        )

    # Use the paginate_query function to handle pagination
    paginated_result = paginate_query(query, page, limit)
    # Check if any students are found
    if not paginated_result['items']:
        return jsonify({"error": "No student found"}), 404

    student_list = []

    for id, name, f_name, G_name, section, section_id, grade_id, subject_id, total, rank, semester, year in paginated_result['items']:
        student_list.append({
            "student_id": id,
            "name": name,
            "father_name": f_name,
            "grand_father_name": G_name,
            "section": section,
            "section_id": section_id,
            "grade_id": grade_id,
            "subject_id": subject_id,
            "total_score": total,
            "rank": rank,
            "semester": semester,
            "year": year
        })

    return jsonify({
        "students": student_list,
        "meta": paginated_result['meta'],
        "header": {
            "grade": data['grade'][0],
            "year": data['year'][0],
            "subject": 'None',
        },
    }
    ), 200


@teach.route('/student/assessment', methods=['GET'])
@teacher_required
def get_student_mark_list(teacher_data):
    url = request.url
    parsed_url = urlparse(url)
    data = parse_qs(parsed_url.query)

    required_data = {
        'student_id',
        'grade_id',
        'subject_id',
        'section_id',
        'semester',
        'year'
    }

    for field in required_data:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400

    student_id = data['student_id'][0]
    grade_id = data['grade_id'][0]
    subject_id = data['subject_id'][0]
    section_id = data['section_id'][0]
    semester = data['semester'][0]
    year = data['year'][0]
    try:
        query = (
            storage.get_session()
            .query(MarkList.type,
                   MarkList.score,
                   MarkList.percentage,
                   )
            .join(TeachersRecord, TeachersRecord.id == MarkList.teachers_record_id)
            .filter(MarkList.student_id == student_id,
                    MarkList.grade_id == grade_id,
                    MarkList.subject_id == subject_id,
                    MarkList.section_id == section_id,
                    MarkList.semester == semester,
                    MarkList.year == year,
                    TeachersRecord.teacher_id == teacher_data.id
                    )
            .order_by(MarkList.percentage.asc(), MarkList.type.asc())
        ).all()

        assessment = []
        for type, score, percentage in query:
            assessment.append({
                "assessment_type": type,
                "score": score,
                "percentage": percentage,
            })
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve student assessment"}), 500

    return jsonify({"assessment": assessment}), 200


@teach.route('/assigned-subject', methods=['GET'])
@teacher_required
def teacher_assigned_subjects(teacher_data):
    query = (
        storage.get_session()
        .query(Subject.name, Subject.id)
        .join(TeachersRecord, TeachersRecord.subject_id == Subject.id)
        .join(Teacher, Teacher.id == TeachersRecord.teacher_id)
        .filter(Teacher.id == teacher_data.id)
        .distinct(Subject.id)
    ).all()

    assigned_subjects = []
    for name, id in query:
        assigned_subjects.append({
            "id": id,
            "name": name
        })

    return jsonify(assigned_subjects), 200


@teach.route('/assigned', methods=['GET'])
@teacher_required
def get_teacher_assigned_grade(teacher_data):
    """
    Retrieve the grades assigned to a specific teacher.

    Args:
        teacher_data (object): An object containing the teacher's data, 
                               specifically the teacher's ID.

    Returns:
        Response: A JSON response containing the list of grades assigned to the teacher 
                  if found, or an error message if no grades were assigned.
        int: HTTP status code 200 if grades are found, 404 if no grades are assigned.
    """
    assigned_grade = (
        storage.get_session()
        .query(Grade.grade, Section.section)
        .join(TeachersRecord, TeachersRecord.grade_id == Grade.id)
        .join(Section, Section.id == TeachersRecord.section_id)
        .filter(TeachersRecord.teacher_id == teacher_data.id)
        .distinct(Grade.id)
    )
    if not assigned_grade.all():
        return jsonify({"error": f"No grades were assigned"}), 404

    assigned = {}
    for grade, section in assigned_grade:
        if grade not in assigned:
            assigned[grade] = []
        assigned[grade].append(section)

    print(assigned)
    return jsonify(assigned), 200


@teach.route('/students/mark_list', methods=['PUT'])
@teacher_required
def update_student_assessment(teacher_data):
    """
    Adds or updates student assessment scores for a given teacher.

    Args:
        teacher_data (object): The teacher data object containing the teacher's information.

    Returns:
        Response: A JSON response indicating the success or failure of the operation.

    Raises:
        Exception: If an unexpected error occurs during the update process.

    The function performs the following steps:
    1. Retrieves JSON data from the request.
    2. Validates the presence of required fields in the JSON data.
    3. Fetches the teacher's record based on the provided teacher data and student data.
    4. Updates the student's assessment scores in the database.
    5. Commits the updates to the database.
    6. Calculates and updates the student's subject sum, semester average, and yearly average.
    7. Handles any exceptions that occur during the process and returns an appropriate error response.

    Returns:
        Response: A JSON response indicating the success or failure of the operation.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 404
    required_data = {
        "student_data",
        "assessments",
    }

    for field in required_data:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400

    student_data = data.get('student_data')
    assessments = data.get('assessments')

    try:
        teacher_record = storage.get_session().query(TeachersRecord).filter(
            TeachersRecord.teacher_id == teacher_data.id,
            TeachersRecord.grade_id == student_data['grade_id'],
            TeachersRecord.section_id == student_data['section_id'],
            TeachersRecord.subject_id == student_data['subject_id']
        ).first()

        if not teacher_record:
            return jsonify({"error": "Teacher record not found"}), 404

        for assessment in assessments:
            update_score = storage.get_session().execute(
                update(MarkList)
                .where(and_(
                    MarkList.teachers_record_id == teacher_record.id,
                    MarkList.student_id == student_data['student_id'],
                    MarkList.semester == student_data['semester'],
                    MarkList.year == student_data['year'],
                    MarkList.type == assessment['assessment_type']
                ))
                .values(score=assessment['score'], updated_at=datetime.utcnow().isoformat())
            )

            if update_score.rowcount == 0:
                return jsonify({"error": f"Failed to update score for assessment type {assessment['type']} for student {student_data['name']}"}), 500

            # Commit the updates to the database
            storage.save()

        subject_sum(student_data)
        semester_average(student_data)
        yearly_average(student_data)

    except Exception as e:
        return jsonify({"error": f"Unexpected error occurred Failed to update score"}), 500

    return jsonify({"message": "Student Score Updated Successfully."}), 201


def subject_sum(student_data):
    """
    Calculate the total score for a specific subject and student, and update or create an Assessment record.

    This function queries the MarkList table to sum the scores for a given student, subject, semester, and year.
    It then updates or creates an Assessment record with the total score. Finally, it calls the subject_ranks
    function to update the subject ranks.

    Args:
        student_data (dict): A dictionary containing the following keys:
            - student_id (int): The ID of the student.
            - subject_id (int): The ID of the subject.
            - semester (int): The semester number.
            - year (int): The academic year.

    Returns:
        None
    """
    total = storage.get_session().query(
        MarkList.subject_id,
        MarkList.student_id,
        MarkList.year,
        MarkList.semester,
        func.sum(MarkList.score).label('total_score')
    ).filter(
        MarkList.student_id == student_data['student_id'],
        MarkList.subject_id == student_data['subject_id'],
        MarkList.semester == student_data['semester'],
        MarkList.year == student_data['year']
    ).group_by(MarkList.subject_id).all()

    for sum in total:
        overall = storage.get_session().query(Assessment).filter_by(
            student_id=sum.student_id,
            subject_id=sum.subject_id,
            semester=sum.semester,
            year=sum.year,
        ).first()

        if not overall:
            overall = Assessment(
                student_id=sum.student_id,
                subject_id=sum.subject_id,
                semester=sum.semester,
                year=sum.year,
                updated_at=datetime.utcnow().isoformat()
            )
            storage.add(overall)
        else:
            overall.total = sum.total_score

    storage.save()
    subject_ranks(student_data)


def semester_average(student_data):
    """
    Calculate the average score for a student in a specific semester and year,
    update or create an AVRGResult entry with the calculated average, and 
    subsequently update the semester ranks.

    Args:
        student_data (dict): A dictionary containing the student's ID, semester, 
                             and year. Example:
                             {
                                 'student_id': <student_id>,
                                 'semester': <semester>,
                                 'year': <year>
                             }

    Returns:
        None
    """
    average = storage.get_session().query(
        Assessment.student_id,
        Assessment.year,
        Assessment.semester,
        func.avg(Assessment.total).label('average_score')
    ).filter(
        Assessment.student_id == student_data['student_id'],
        Assessment.semester == student_data['semester'],
        Assessment.year == student_data['year']
    ).group_by(Assessment.semester).all()

    for avg in average:
        overall = storage.get_session().query(AVRGResult).filter_by(
            student_id=avg.student_id,
            semester=avg.semester,
            year=avg.year,
        ).first()

        if not overall:
            overall = AVRGResult(
                student_id=avg.student_id,
                semester=avg.semester,
                year=avg.year,
                updated_at=datetime.utcnow().isoformat()
            )
            storage.add(overall)
        else:
            overall.average = avg.average_score

    storage.save()
    semester_ranks(student_data)


def yearly_average(student_data):
    """
    Calculate and update the yearly average score for a student.

    This function retrieves the average results for a student for a given year,
    calculates the yearly average, and updates or creates a record in the 
    StudentYearlyRecord table with the calculated average. It also triggers 
    the year_ranks function to update the student's ranking.

    Args:
        student_data (dict): A dictionary containing 'student_id' and 'year' keys.

    Returns:
        None
    """

    result = storage.get_session().query(AVRGResult).filter_by(
        student_id=student_data['student_id'],
        year=student_data['year']
    ).all()

    if len(result) != 2:
        return

    # Calculate the yearly average
    yearly_avg = sum([res.average for res in result if res.average]) / 2

    overall = storage.get_session().query(StudentYearlyRecord).filter_by(
        student_id=student_data['student_id'],
        year=student_data['year'],
    ).first()

    if not overall:
        overall = StudentYearlyRecord(
            student_id=student_data['student_id'],
            year=student_data['year'],
            final_score=yearly_avg,
            updated_at=datetime.utcnow().isoformat()
        )
        storage.add(overall)
    else:
        overall.final_score = yearly_avg

    storage.save()
    year_ranks(student_data)


def subject_ranks(student_data):
    """
    Calculate and assign ranks to students based on their total scores in a specific subject, semester, and year.

    Args:
        student_data (dict): A dictionary containing the following keys:
            - 'subject_id' (int): The ID of the subject.
            - 'semester' (str): The semester for which the ranks are to be calculated.
            - 'year' (int): The year for which the ranks are to be calculated.

    The function queries the database to get distinct subject IDs matching the provided subject_id, semester, and year.
    For each subject, it retrieves all assessments, orders them by total score in descending order, and assigns ranks
    based on their position in the sorted list. The ranks are then saved back to the database.
    """
    for subject_id in storage.get_session().query(Assessment.subject_id).filter(
        Assessment.subject_id == student_data['subject_id'],
        Assessment.semester == student_data['semester'],
        Assessment.year == student_data['year']
    ).distinct():
        totals = storage.get_session().query(Assessment).filter_by(
            # subject_id is a tuple, we need to access the first element
            subject_id=subject_id[0],
            semester=student_data['semester'],
            year=student_data['year']
        ).order_by(Assessment.total.desc()).all()

        for rank, total in enumerate(totals, start=1):
            total.rank = rank

    storage.save()


def semester_ranks(student_data):
    """
    Calculate and assign ranks to students based on their average results for a given semester and year.

    Args:
        student_data (dict): A dictionary containing 'semester' and 'year' keys to filter the results.

    Returns:
        None: This function updates the ranks in the database and does not return any value.

    Example:
        student_data = {'semester': 'Fall', 'year': 2023}
        semester_ranks(student_data)
    """
    for semester in storage.get_session().query(AVRGResult.semester).filter(
        AVRGResult.semester == student_data['semester'],
        AVRGResult.year == student_data['year']
    ).distinct():
        average = storage.get_session().query(AVRGResult).filter_by(
            semester=semester[0],
            year=student_data['year']
        ).order_by(AVRGResult.average.desc()).all()

        for rank, avrg in enumerate(average, start=1):
            avrg.rank = rank

    storage.save()


def year_ranks(student_data):
    """
    Calculate and assign ranks to students based on their final scores for a given year.

    Args:
        student_data (dict): A dictionary containing student information, specifically the year to filter by.

    Returns:
        None: This function updates the ranks in the database and does not return any value.

    The function performs the following steps:
    1. Queries the database to get distinct years matching the provided year in student_data.
    2. For each year, retrieves student records ordered by their final scores in descending order.
    3. Assigns ranks to students based on their final scores.
    4. Saves the updated ranks back to the database.
    """
    for year in storage.get_session().query(StudentYearlyRecord.year).filter(
        StudentYearlyRecord.year == student_data['year'],
    ).distinct():
        average = storage.get_session().query(StudentYearlyRecord).filter_by(
            year=year[0],
        ).order_by(StudentYearlyRecord.final_score.desc()).all()

        for rank, avrg in enumerate(average, start=1):
            avrg.rank = rank

    storage.save()
