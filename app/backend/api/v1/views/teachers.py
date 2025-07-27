#!/usr/bin/python3
"""Teacher views module for the API"""

from flask import request, jsonify
from sqlalchemy import func, true
from models import storage
from datetime import datetime
from models.user import User
from models.grade import Grade
from models.student import Student
from models.section import Section
from models.subject import Subject
from models.assessment import Assessment
from models.mark_list import MarkList
from models.student_term_record import StudentTermRecord
from models.subject_yearly_average import SubjectYearlyAverage
from models.student_year_record import StudentYearRecord
from urllib.parse import urlparse, parse_qs
from sqlalchemy import update, and_
from flask import Blueprint
from api.v1.schemas.schemas import *
from api.v1.views.utils import teacher_required


teach = Blueprint("teach", __name__, url_prefix="/api/v1/teacher")


@teach.route("/dashboard", methods=["GET"])
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
        return jsonify({"message": "Teacher not found"}), 404
    return jsonify(teacher_data.to_dict()), 200


@teach.route("/profile", methods=["PUT"])
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
        return jsonify({"message": "Not a JSON"}), 400

    required_data = {
        "first_name",
        "email",
        "phone",
    }

    for field in required_data:
        if field not in data:
            return jsonify({"message": f"Missing {field}"}), 400

    teacher_data.first_name = data["first_name"]
    teacher_data.email = data["email"]
    teacher_data.phone = data["phone"]

    if "new_password" in data:
        if "current_password" not in data:
            return jsonify({"message": "Missing old password"}), 400
        user = storage.get_first(User, id=teacher_data.id)
        if not user:
            return jsonify({"message": "User not found"}), 404
        if not user.check_password(data["current_password"]):
            return jsonify({"message": "Incorrect password"}), 400

        user.hash_password(data["new_password"])
    storage.save()

    return jsonify({"message": "Profile Updated Successfully"}), 200


@teach.route("/students", methods=["GET"])
@teacher_required
def get_list_of_students(teacher_data):
    """
    Retrieves a list of students based on the provided teacher data and query parameters.

    Returns:
        Response: A JSON response containing the list of students and relevant header information,
                  or an error message with the appropriate HTTP status code.
    """
    url = request.url
    parsed_url = urlparse(url)
    data = parse_qs(parsed_url.query)

    if not data:
        return jsonify({"message": "Bad Request"}), 400

    required_data = {"subject_code", "grade", "semester", "year"}

    for field in required_data:
        if field not in data:
            return jsonify({"message": f"Missing {field}"}), 400

    subject = storage.get_first(Subject, code=data["subject_code"][0])
    if not subject:
        return jsonify({"message": "Subject not found"}), 404

    query = (
        storage.session.query(
            Student.id.label("student_id"),
            Student.name,
            Student.father_name.label("fatherName"),
            Student.grand_father_name.label("grandFatherName"),
            Grade.id.label("grade_id"),
            Section.section,
            Section.id.label("section_id"),
            Assessment.subject_id.label("subject_id"),
            Assessment.total,
            Assessment.rank,
            Assessment.semester,
            Assessment.year,
        )  # Explicitly specify the table being queried
        .select_from(Assessment)
        .join(TeachersRecord, TeachersRecord.id == Assessment.teachers_record_id)
        .join(Student, Student.id == Assessment.student_id)
        .join(Grade, Grade.id == Assessment.grade_id)
        .join(Section, Section.id == Assessment.section_id)
        .filter(
            and_(
                true(),
                TeachersRecord.teacher_id == teacher_data.id,
                Assessment.subject_id == subject.id,
                Assessment.semester == data["semester"][0],
                Grade.grade == data["grade"][0],
            )
        )
        .order_by(
            Student.name.asc(),
            Student.father_name.asc(),
            Student.grand_father_name.asc(),
            Student.id.asc(),
        )
    )

    student_list = [{key: value for key, value in q._asdict().items()} for q in query]

    return jsonify(
        {
            "students": student_list,
            "meta": {},
            "header": {
                "grade": data["grade"][0],
                "year": data["year"][0],
                "subject": "None",
            },
        }
    ), 200


@teach.route("/student/assessment", methods=["GET"])
@teacher_required
def get_student_assessment(teacher_data):
    url = request.url
    parsed_url = urlparse(url)
    data = parse_qs(parsed_url.query)

    required_data = {
        "student_id",
        "grade_id",
        "subject_id",
        # 'section_id',
        "semester",
        "year",
    }

    for field in required_data:
        if field not in data:
            return jsonify({"message": f"Missing {field}"}), 400

    student_id = data["student_id"][0]
    grade_id = data["grade_id"][0]
    subject_id = data["subject_id"][0]
    # section_id = data['section_id'][0]
    semester = data["semester"][0]
    year = data["year"][0]
    try:
        query = (
            storage.session.query(
                MarkList.type,
                MarkList.score,
                MarkList.percentage,
            )
            .join(TeachersRecord, TeachersRecord.id == MarkList.teachers_record_id)
            .filter(
                MarkList.student_id == student_id,
                MarkList.grade_id == grade_id,
                MarkList.subject_id == subject_id,
                # MarkList.section_id == section_id,
                MarkList.semester == semester,
                MarkList.year == year,
                TeachersRecord.teacher_id == teacher_data.id,
            )
            .order_by(MarkList.percentage.asc(), MarkList.type.asc())
        ).all()

        assessment = []
        for type, score, percentage in query:
            assessment.append(
                {
                    "assessment_type": type,
                    "score": score,
                    "percentage": percentage,
                }
            )
    except Exception:
        return jsonify({"message": "Failed to retrieve student assessment"}), 500

    return jsonify({"assessment": assessment}), 200


@teach.route("/students/assigned", methods=["GET"])
@teacher_required
def teacher_assigned(teacher_data):
    query = (
        storage.session.query(Subject.name, Subject.code, Grade.grade, Section.section)
        .join(TeachersRecord, TeachersRecord.subject_id == Subject.id)
        .join(Grade, Grade.id == TeachersRecord.grade_id)
        .join(Section, Section.id == TeachersRecord.section_id)
        .filter(TeachersRecord.teacher_id == teacher_data.id)
        .distinct(Subject.id)
    ).all()

    assigned = {}
    for subject, code, grade, section in query:
        if subject not in assigned:
            assigned[subject] = {"grades": [], "sections": [], "subject_code": ""}
        if grade not in assigned[subject]["grades"]:
            assigned[subject]["grades"].append(grade)
        if not assigned[subject]["subject_code"]:
            assigned[subject]["subject_code"] = code
        assigned[subject]["sections"].append(section)

    return jsonify(assigned), 200


@teach.route("/students/mark_list", methods=["PUT"])
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
        return jsonify({"message": "Not a JSON"}), 404
    required_data = {
        "student_data",
        "assessments",
    }

    for field in required_data:
        if field not in data:
            return jsonify({"message": f"Missing {field}"}), 400

    student_data = data.get("student_data")
    assessments = data.get("assessments")

    required_student_data = {
        "student_id",
        "grade_id",
        "section_id",
        "subject_id",
        "semester",
        "year",
    }

    for field in required_student_data:
        if field not in student_data:
            return jsonify({"message": f"Missing {field}"}), 400

    try:
        teacher_record = (
            storage.session.query(TeachersRecord)
            .filter(
                TeachersRecord.teacher_id == teacher_data.id,
                TeachersRecord.grade_id == student_data["grade_id"],
                TeachersRecord.section_id == student_data["section_id"],
                TeachersRecord.subject_id == student_data["subject_id"],
                TeachersRecord.semester == student_data["semester"],
            )
            .first()
        )

        if not teacher_record:
            return jsonify({"message": "Teacher record not found"}), 404

        for assessment in assessments:
            update_score = storage.session.execute(
                update(MarkList)
                .where(
                    and_(
                        MarkList.teachers_record_id == teacher_record.id,
                        MarkList.student_id == student_data["student_id"],
                        MarkList.semester == student_data["semester"],
                        MarkList.year == student_data["year"],
                        MarkList.type == assessment["assessment_type"],
                    )
                )
                .values(
                    score=assessment["score"], updated_at=datetime.utcnow().isoformat()
                )
            )

            if update_score.rowcount == 0:
                return jsonify(
                    {
                        "message": f"Failed to update score for assessment type {assessment['type']} for student {student_data['name']}"
                    }
                ), 500

            # Commit the updates to the database
            storage.save()

        subject_sum(student_data)
        subject_average(student_data)
        semester_average(student_data)
        yearly_average(student_data)

    except Exception as e:
        print(e)
        return jsonify(
            {"message": "Unexpected error occurred Failed to update score"}
        ), 500

    return jsonify({"message": "Student Score Updated Successfully."}), 201


def subject_sum(student_data):
    """
    Calculate the total score for a specific subject and student, and update or create an Assessment record.

    This function queries the MarkList table to sum the scores for a given student, subject, semester, and year.
    It then updates or creates an Assessment record with the total score. Finally, it calls the total_subject_ranks
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
    total = (
        storage.session.query(func.sum(MarkList.score).label("total_score"))
        .filter(
            MarkList.student_id == student_data["student_id"],
            MarkList.subject_id == student_data["subject_id"],
            MarkList.semester == student_data["semester"],
            MarkList.year == student_data["year"],
        )
        .group_by(MarkList.subject_id)
        .first()
    )

    storage.session.execute(
        update(Assessment)
        .where(
            and_(
                Assessment.student_id == student_data["student_id"],
                Assessment.subject_id == student_data["subject_id"],
                Assessment.semester == student_data["semester"],
                Assessment.year == student_data["year"],
            )
        )
        .values(total=total.total_score, updated_at=datetime.utcnow().isoformat())
    )

    storage.save()

    total_subject_ranks(student_data)


def total_subject_ranks(student_data):
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
    ranked_data_subquery = (
        storage.session.query(
            Assessment.student_id,
            Assessment.subject_id,
            Assessment.semester,
            Assessment.year,
            func.rank().over(order_by=Assessment.total.desc()).label("new_rank"),
        )
        .where(
            and_(
                Assessment.subject_id == student_data["subject_id"],
                Assessment.total.isnot(None),
            )
        )
        .subquery()
    )

    storage.session.execute(
        update(Assessment)
        .where(
            and_(
                Assessment.student_id
                == ranked_data_subquery.c.student_id,  # c is short for Column
                Assessment.subject_id == ranked_data_subquery.c.subject_id,
                Assessment.semester == ranked_data_subquery.c.semester,
                Assessment.year == ranked_data_subquery.c.year,
            )
        )
        .values(
            rank=ranked_data_subquery.c.new_rank,
            updated_at=datetime.utcnow().isoformat(),
        )
    )

    storage.save()


def subject_average(student_data):
    average_subject = (
        storage.session.query(
            Assessment.student_id,
            Assessment.subject_id,
            Assessment.year,
            func.avg(Assessment.total).label("average_subject"),
        )
        .filter(
            Assessment.student_id == student_data["student_id"],
            Assessment.subject_id == student_data["subject_id"],
            Assessment.year == student_data["year"],
        )
        .group_by(Assessment.subject_id)
        .having(func.count(Assessment.total) == func.count())
    ).first()

    if average_subject:
        storage.session.execute(
            update(SubjectYearlyAverage)
            .where(
                and_(
                    SubjectYearlyAverage.student_id == average_subject.student_id,
                    SubjectYearlyAverage.subject_id == average_subject.subject_id,
                    SubjectYearlyAverage.year == average_subject.year,
                )
            )
            .values(
                average=average_subject.average_subject,
                updated_at=datetime.utcnow().isoformat(),
            )
        )

        storage.save()

        average_subject_ranks(student_data)


def average_subject_ranks(student_data):
    ranked_data_subquery = (
        storage.session.query(
            SubjectYearlyAverage.student_id,
            SubjectYearlyAverage.subject_id,
            SubjectYearlyAverage.year,
            func.rank().over(order_by=SubjectYearlyAverage.average.desc()).label("new_rank"),
        )
        .where(
            and_(
                SubjectYearlyAverage.subject_id == student_data["subject_id"],
                SubjectYearlyAverage.average.isnot(None),
            )
        )
        .subquery()
    )

    storage.session.execute(
        update(SubjectYearlyAverage)
        .where(
            and_(
                SubjectYearlyAverage.student_id
                == ranked_data_subquery.c.student_id,  # c is short for Column
                SubjectYearlyAverage.subject_id == ranked_data_subquery.c.subject_id,
                SubjectYearlyAverage.year == ranked_data_subquery.c.year,
            )
        )
        .values(
            rank=ranked_data_subquery.c.new_rank,
            updated_at=datetime.utcnow().isoformat(),
        )
    )

    storage.save()


def semester_average(student_data):
    """
    Calculate the average score for a student in a specific semester and year,
    update or create an StudentTermRecord entry with the calculated average, and
    subsequently update the semester ranks.

    Returns:
        None
    """
    average = (
        storage.session.query(
            Assessment.student_id,
            Assessment.semester,
            Assessment.year,
            func.avg(Assessment.total).label("average_score"),
        )
        .filter(
            Assessment.student_id == student_data["student_id"],
            Assessment.semester == student_data["semester"],
            Assessment.year == student_data["year"],
        )
        .group_by(Assessment.semester)
        # Check if all marks are entered
        .having(func.count(Assessment.total) == func.count())
    ).first()

    if average:
        storage.session.execute(
            update(StudentTermRecord)
            .where(
                and_(
                    StudentTermRecord.student_id == average.student_id,
                    StudentTermRecord.semesters == average.semester,
                    StudentTermRecord.year == average.year,
                )
            )
            .values(
                average=average.average_score, updated_at=datetime.utcnow().isoformat()
            )
        )

        storage.save()

        semester_ranks(student_data)


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
    ranked_data_subquery = (
        storage.session.query(
            StudentTermRecord.student_id,
            StudentTermRecord.semesters,
            StudentTermRecord.year,
            func.rank()
            .over(order_by=StudentTermRecord.average.desc())
            .label("new_rank"),
        )
        .where(
            and_(
                StudentTermRecord.semesters == student_data["semester"],
                StudentTermRecord.year == student_data["year"],
                StudentTermRecord.average.isnot(None),
            )
        )
        .subquery()
    )

    storage.session.execute(
        update(StudentTermRecord)
        .where(
            and_(
                # c is short for Column
                StudentTermRecord.student_id == ranked_data_subquery.c.student_id,
                StudentTermRecord.semesters == ranked_data_subquery.c.semester,
                StudentTermRecord.year == ranked_data_subquery.c.year,
            )
        )
        .values(
            rank=ranked_data_subquery.c.new_rank,
            updated_at=datetime.utcnow().isoformat(),
        )
    )

    storage.save()


def yearly_average(student_data):
    """
    Calculate and update the yearly average score for a student.

    This function retrieves the average results for a student for a given year,
    calculates the yearly average, and updates or creates a record in the
    StudentYearRecord table with the calculated average. It also triggers
    the year_ranks function to update the student's ranking.

    Args:
        student_data (dict): A dictionary containing 'student_id' and 'year' keys.

    Returns:
        None
    """

    average = (
        storage.session.query(
            StudentTermRecord.student_id,
            StudentTermRecord.year,
            func.avg(StudentTermRecord.average).label("semester_average"),
        )
        .filter(
            StudentTermRecord.student_id == student_data["student_id"],
            StudentTermRecord.year == student_data["year"],
        )
        .group_by(StudentTermRecord.student_id)
        .first()
    )

    if average:
        storage.session.execute(
            update(StudentYearRecord)
            .where(
                and_(
                    StudentYearRecord.student_id == average.student_id,
                    StudentYearRecord.year == average.year,
                )
            )
            .values(
                final_score=average.semester_average,
                updated_at=datetime.utcnow().isoformat(),
            )
        )

        storage.save()
        year_ranks(student_data)


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
    ranked_data_subquery = (
        storage.session.query(
            StudentYearRecord.student_id,
            StudentYearRecord.year,
            func.rank()
            .over(order_by=StudentYearRecord.final_score.desc())
            .label("new_rank"),
        )
        .where(
            and_(
                StudentYearRecord.year == student_data["year"],
                StudentYearRecord.final_score.isnot(None),
            )
        )
        .subquery()
    )

    storage.session.execute(
        update(StudentYearRecord)
        .where(
            and_(
                # c is short for Column
                StudentYearRecord.student_id == ranked_data_subquery.c.student_id,
                StudentTermRecord.year == ranked_data_subquery.c.year,
            )
        )
        .values(
            rank=ranked_data_subquery.c.new_rank,
            updated_at=datetime.utcnow().isoformat(),
        )
    )

    storage.save()
