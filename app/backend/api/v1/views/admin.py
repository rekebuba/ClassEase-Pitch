#!/usr/bin/python3
"""Admin views module for the API"""

from typing import Tuple
import uuid
from flask import Response, request, jsonify, url_for
from marshmallow import ValidationError
from sqlalchemy import case, func
from api.v1.utils.typing import UserT
from models.year import Year
from models import storage
from flask import Blueprint
from models.user import User
from models.subject import Subject
from models.teacher import Teacher
from models.grade import Grade
from models.student import Student
from models.section import Section
from models.mark_list import MarkList
from models.assessment import Assessment
from models.stud_semester_record import STUDSemesterRecord
from models.average_subject import AVRGSubject
from models.stud_year_record import STUDYearRecord
from models.teacher_record import TeachersRecord
from models.event import Event
from models.semester import Semester
from datetime import datetime
from sqlalchemy import update, select, and_
from sqlalchemy.orm import joinedload
from urllib.parse import urlparse, parse_qs
from api.v1.views.utils import admin_required
from api.v1.views.methods import (
    make_case_lookup,
    min_max_semester_lookup,
    min_max_year_lookup,
    paginate_query,
)
from api.v1.schemas.schemas import *  # noqa: F401
from api.v1.views import errors


admin = Blueprint("admin", __name__, url_prefix="/api/v1/admin")


@admin.route("/profile", methods=["PUT"])
@admin_required
def update_admin_profile(admin_data: UserT) -> Tuple[Response, int]:
    """
    Update the profile of an admin user.

    Args:
        admin_data (object): The admin user object whose profile is to be updated.

    Returns:
        Response: A JSON response indicating the result of the update operation.
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "Not a JSON"}), 400
    return jsonify({"message": "Profile Updated Successfully"}), 200


@admin.route("/overview", methods=["GET"])
@admin_required
def school_overview(admin_data: UserT) -> Tuple[Response, int]:
    """
    Provides an overview of the school including total number of teachers, total number of students,
    enrollment statistics by grade, and performance statistics by subject.

    Args:
        admin_data (dict): Data related to the admin requesting the overview.
    """
    total_teachers = storage.get_all(Teacher)
    total_students = storage.get_all(Student)
    enrollment_by_grade = (
        storage.session.query(Grade.grade, func.count(STUDYearRecord.student_id))
        .join(Grade, STUDYearRecord.grade_id == Grade.id)
        .group_by(
            STUDYearRecord.grade_id,
        )
        .all()
    )

    performance_by_subject = (
        storage.session.query(Subject.name, func.avg(MarkList.score))
        .join(Subject, MarkList.subject_id == Subject.id)
        .group_by(Subject.name)
        .all()
    )

    return jsonify(
        {
            "total_teachers": len(total_teachers),
            "total_students": len(total_students),
            "enrollment_by_grade": [
                {"grade": grade, "student_count": student_count}
                for grade, student_count in enrollment_by_grade
            ],
            "performance_by_subject": [
                {"subject": subject, "average_percentage": average_percentage}
                for subject, average_percentage in performance_by_subject
            ],
        }
    ), 200


@admin.route("/assign-teacher", methods=["PUT"])
@admin_required
def assign_class(admin_data: UserT) -> Tuple[Response, int]:
    """
    Assigns a teacher to a class based on the provided data.

    Args:
        admin_data (dict): Data containing information about the teacher and class assignment.

    Returns:
        Response: JSON response indicating success or failure of the operation.
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "Not a JSON"}), 400

    required_data = [
        "teacher_id",
        "grade",
        "section",
        "subjects_taught",
        "semester",
        "mark_list_year",
    ]
    # Check if required fields are present
    for field in required_data:
        if field not in data:
            return jsonify({"message": f"Missing {field}"}), 400

    # Get the teacher by ID
    teacher = storage.get_first(Teacher, id=data["teacher_id"])
    if not teacher:
        return jsonify({"message": "Teacher not found"}), 404

    # Get the grade_id from the Grade table
    grade_id = (
        storage.session.execute(select(Grade.id).where(Grade.grade == data["grade"]))
        .scalars()
        .first()
    )
    if not grade_id:
        return jsonify({"message": "No grade found for the teacher"}), 404

    # get the subject_id
    subjects_taught = (
        storage.session.query(Subject)
        .filter(Subject.grade_id == grade_id, Subject.name.in_(data["subjects_taught"]))
        .all()
    )
    if not subjects_taught:
        return jsonify({"message": "Subject not found"}), 404

    try:
        for subject in subjects_taught:
            # get the section_id
            section_ids = [
                id[0]
                for id in storage.session.query(Section.id)
                .filter(
                    Section.grade_id == grade_id, Section.section.in_(data["section"])
                )
                .all()
            ]

            if not section_ids:
                return jsonify(
                    {
                        "message": f"Section not found, Mark List was not created for the grade {data['grade']}"
                    }
                ), 404

            for section_id in section_ids:
                # check if the another teacher is already assigned to the subject
                teacher_record = storage.get_first(
                    TeachersRecord,
                    grade_id=grade_id,
                    section_id=section_id,
                    subject_id=subject.id,
                    semester=data["semester"],
                )
                # update the teacher record
                if teacher_record:
                    return jsonify({"message": "Teacher already assigned"}), 409
                teacher_record = TeachersRecord(
                    teacher_id=teacher.id,
                    grade_id=grade_id,
                    section_id=section_id,
                    subject_id=subject.id,
                    semester=data["semester"],
                )

                storage.add(teacher_record)

                # Update the MarkList table
                storage.session.execute(
                    update(MarkList)
                    .where(
                        and_(
                            MarkList.grade_id == grade_id,
                            MarkList.section_id == section_id,
                            MarkList.subject_id == subject.id,
                            MarkList.semester == data["semester"],
                            MarkList.year == data["mark_list_year"],
                        )
                    )
                    .values(teachers_record_id=teacher_record.id)
                )

                # Update the Assessment table
                storage.session.execute(
                    update(Assessment)
                    .where(
                        and_(
                            Assessment.grade_id == grade_id,
                            Assessment.subject_id == subject.id,
                            Assessment.semester == data["semester"],
                            Assessment.year == data["mark_list_year"],
                        )
                    )
                    .values(teachers_record_id=teacher_record.id)
                )

                # Update the AVRGSubject table
                storage.session.execute(
                    update(AVRGSubject)
                    .where(
                        and_(
                            AVRGSubject.grade_id == grade_id,
                            AVRGSubject.subject_id == subject.id,
                            AVRGSubject.year == data["mark_list_year"],
                        )
                    )
                    .values(teachers_record_id=teacher_record.id)
                )

                # Commit the final updates to the database
                storage.save()
    except Exception as e:
        storage.rollback()
        return jsonify({"message": "error internal server"}), 500

    return jsonify({"message": "Teacher assigned successfully!"}), 201


@admin.route("/events", methods=["GET"])
@admin_required
def available_events(admin_data: UserT) -> Tuple[Response, int]:
    """
    Handle retrieval of events.

    Args:
        admin_data (object): The admin data object.

    Returns:
        Response: A JSON response list of events or an error message.
    """
    try:
        events = storage.session.query(Event).all()

        if not events:
            return errors.handle_not_found_error("No event found")

        schema = AvailableEventsSchema()
        result = schema.dump({"events": events})

        return jsonify(result), 200
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)


@admin.route("/event/new", methods=["POST"])
@admin_required
def create_events(admin_data: UserT) -> Tuple[Response, int]:
    try:
        data = request.get_json()
        event_schema = EventSchema()
        validated_data = event_schema.load(data)

        # extract any nested felids
        semester = validated_data.pop("semester", None)

        new_event = Event(**validated_data)
        storage.add(new_event)
        storage.session.flush()

        if new_event.purpose == "New Semester":
            semester_data = {
                **semester,
                "event_id": new_event.id,
            }

            # check for duplicate event
            existing_event = (
                storage.session.query(Event, Semester, Year)
                .join(Semester, Semester.event_id == Event.id)
                .join(Year, Year.id == Event.year_id)
                .filter(
                    and_(
                        Event.purpose == new_event.purpose,
                        Event.organizer == new_event.organizer,
                    )
                )
            )

            new_semester = Semester(**semester_data)
            storage.add(new_semester)

        storage.save()

        return event_schema.dump({"message": "Event Created Successfully"}), 201
    except ValidationError as e:
        storage.rollback()
        return errors.handle_validation_error(e)
    except Exception as e:
        storage.rollback()
        return errors.handle_internal_error(e)


@admin.route("/registered_grades", methods=["GET"])
@admin_required
def registered_grades(admin_data: UserT) -> Tuple[Response, int]:
    """
    Retrieve and return a list of registered grades.

    Args:
        admin_data (dict): Data related to the admin making the request.

    Returns:
        Response: A JSON response containing a list of registered grades.
    """
    try:
        registered_grades = (
            storage.session.query(Grade)
            .join(Student, Student.current_grade_id == Grade.id)
            .filter(Student.is_registered == True)
            .group_by(Grade.id)
            .all()
        )

        if not registered_grades:
            return errors.handle_not_found_error("No registered grades found")

        schema = RegisteredGradesSchema()
        result = schema.dump(
            {"grades": [grade.to_dict()["grade"] for grade in registered_grades]}
        )

        return jsonify(result), 200
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)


@admin.route("/mark-list/new", methods=["POST"])
@admin_required
def create_mark_list(admin_data: UserT) -> Tuple[Response, int]:
    """
    Create a mark list for students based on the provided data.

    Args:
        admin_data (dict): The data provided by the admin to create the mark list.

    Returns:
        Response: A JSON response indicating the success or failure of the operation.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Not a JSON"}), 404

        mark_list_schema = CreateMarkListSchema()
        validated_data = mark_list_schema.load(data)
        mark_list = []
        for assessment in validated_data["mark_assessment"]:
            registered_students = storage.get_all(
                STUDSemesterRecord,
                grade_id=assessment["grade_id"],
                semester_id=validated_data["semester_id"],
            )
            for student in registered_students:
                for subject in assessment["subjects"]:
                    for assessment_type in assessment["assessment_type"]:
                        new_mark_list = MarkList(
                            user_id=student.user_id,
                            semester_record_id=student.id,
                            subject_id=subject["subject_id"],
                            type=assessment_type["type"],
                            percentage=assessment_type["percentage"],
                        )

                        mark_list.append(new_mark_list)

        storage.session.bulk_save_objects(mark_list)
        storage.save()

        return jsonify({"message": "Mark list created successfully!"}), 201
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)


@admin.route("/students/mark_list", methods=["GET"])
@admin_required
def show_mark_list(admin_data: UserT) -> Tuple[Response, int]:
    """
    Retrieve and display a list of marks for students based on the provided query parameters.

    Args:
        admin_data (dict): Data related to the admin making the request.

    Returns:
        Response: A JSON response containing the list of student marks or an error message with the appropriate HTTP status code.
    """
    url = request.url
    parsed_url = urlparse(url)
    data = parse_qs(parsed_url.query)

    required_data = [
        "grade",
        "sections",
        "subject",
        "assessment_type",
        "semester",
        "year",
    ]
    # Check if required fields are present
    for field in required_data:
        if field not in data:
            return jsonify({"message": f"Missing {field}"}), 400

    grade = storage.get_first(Grade, grade=data["grade"][0])
    if not grade:
        return jsonify({"message": "Grade not found"}), 404

    section = storage.get_first(
        Section, grade_id=grade.id, section=data["section"][0], year=data["year"][0]
    )
    if not section:
        return jsonify({"message": "Section not found"}), 404

    subject = storage.get_first(Subject, grade_id=grade.id, name=data["subject"][0])
    if not subject:
        return jsonify({"message": "Subject not found"}), 404

    students = storage.get_all(
        MarkList,
        grade_id=grade.id,
        section_id=section.id,
        subject_id=subject.id,
        semester=data["semester"][0],
        year=data["year"][0],
    )
    if not students:
        return jsonify({"message": "Student not found"}), 404

    student_list = []
    for student in students:
        student_list.append(student.to_dict())

    return jsonify(student_list), 200


@admin.route("/students", methods=["POST"])
@admin_required
def admin_student_list(admin_data: UserT) -> Tuple[Response, int]:
    """
    Retrieve and filter student data based on the provided admin data.

        Response: A JSON response containing the filtered student data, or an error message if any required data is missing or not found.
    """
    try:
        data = request.get_json()
        # Check if required fields are present
        schema = ParamSchema()
        valid_data = schema.load(data)

        custom_types = {
            **make_case_lookup(1, Section.section, "section"),
            **make_case_lookup(1, STUDSemesterRecord.average, "average"),
            **make_case_lookup(1, STUDSemesterRecord.rank, "rank"),
        }

        # custom sort
        for custom_sort in valid_data["custom_sorts"]:
            column_name = custom_sort["column_name"]
            is_desc = custom_sort.get("desc", False)

            expr = custom_types.get(column_name)
            if expr is None:
                raise ValidationError(f"Invalid custom sort: {custom_sort}")

            valid_data["valid_sorts"].append(expr.desc() if is_desc else expr)

        # custom filter
        result = []
        for custom_filter in valid_data["custom_filters"]:
            column_name = custom_filter["column_name"]
            operator = custom_filter["operator"]
            value = custom_filter["value"]

            expr = custom_types.get(column_name)
            if expr is None:
                raise ValidationError(f"Invalid custom filter: {custom_filter}")

            op_func = OPERATOR_MAPPING.get(operator)
            if op_func is None:
                raise ValidationError(f"Unsupported operator: {operator}")

            try:
                condition = op_func(expr, value)
            except Exception as e:
                raise ValidationError(f"Invalid value for operator '{operator}': {e}")

            result.append(condition)

        valid_data["custom_filters"] = result

        print("valid_data: ", valid_data)

        query = (
            storage.session.query(
                User,
                Student,
                STUDYearRecord,
                Grade,
                custom_types["sectionI"],
                custom_types["sectionII"],
                custom_types["averageI"],
                custom_types["averageII"],
                custom_types["rankI"],
                custom_types["rankII"],
            )
            .join(User.students)  # User → Student
            .outerjoin(Student.year_records)  # Student → STUDYearRecord
            .outerjoin(STUDYearRecord.semester_records)
            .outerjoin(STUDSemesterRecord.sections)  # SemesterRecord → Section
            # SemesterRecord → Semester
            .outerjoin(STUDSemesterRecord.semesters)
            .outerjoin(Section.grade)  # Section → Grade
            .group_by(
                User.id,
                Student.id,
                STUDYearRecord.id,
                Grade.id,
            )
            .options(
                joinedload(User.students)
                .joinedload(Student.year_records)
                .joinedload(STUDYearRecord.semester_records)
                .joinedload(STUDSemesterRecord.sections)
                .joinedload(Section.grade)
            )
        )
        # Check if any students are found
        if not query:
            return jsonify({"data": [], "table_id": {}, "pageCount": 1}), 200

        # Use the paginate_query function to handle pagination
        paginated_result = paginate_query(
            query,
            valid_data["page"],
            valid_data["per_page"],
            valid_data["valid_filters"],
            valid_data["custom_filters"],
            valid_data["valid_sorts"],
            valid_data["join_operator"],
        )

        if not paginated_result["items"]:
            return jsonify({"data": [], "table_id": {}, "pageCount": 1}), 200

        # Process results as needed
        data_to_serialize = [
            {
                "user": user.to_dict(),
                "student": student.to_dict(),
                "grade": grade.to_dict(),
                "year_record": year_record.to_dict(),
                "sectionI": section_I,
                "sectionII": section_II,
                "averageI": average_I,
                "averageII": average_II,
                "rankI": rank_I,
                "rankII": rank_II,
            }
            for user, student, year_record, grade, section_I, section_II, average_I, average_II, rank_I, rank_II in paginated_result[
                "items"
            ]
        ]

        schema = AllStudentsSchema(many=True)
        result = schema.dump(data_to_serialize)
        return jsonify(
            {**result, "pageCount": paginated_result["meta"]["total_pages"]}
        ), 200
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)


@admin.route("/students/status-count", methods=["GET"])
@admin_required
def student_status_count(admin_data: UserT) -> Tuple[Response, int]:
    """
    Retrieve and return the count of students based on their status.

    Returns:
        Response: A JSON response containing the count of students based on their status.
                  If no students are found, returns a 404 error with an appropriate message.
    """
    query = (
        storage.session.query(
            func.count(case((Student.is_active == True, 1), else_=None)).label(
                "active"
            ),
            func.count(case((Student.is_active == False, 1), else_=None)).label(
                "inactive"
            ),
            func.count(case((Student.is_active == None, 1), else_=None)).label(
                "suspended"
            ),
        )
        .join(User.students)
        .outerjoin(Student.year_records)
    )

    # Process results
    result = query.one()
    data_to_serialize = {
        "active": result.active,
        "inactive": result.inactive,
        "suspended": result.suspended,
    }
    # Return the serialized data
    schema = StudentStatusSchema()
    result = schema.load(data_to_serialize)

    return jsonify(**result), 200


@admin.route("/students/average-range", methods=["GET"])
@admin_required
def student_average_range(admin_data: UserT) -> Tuple[Response, int]:
    """
    Retrieve and return the average range of students.

    Returns:
        Response: A JSON response containing the average range of students.
                  If no students are found, returns a 404 error with an appropriate message.
    """
    try:
        custom_types = {
            **min_max_year_lookup(STUDYearRecord.final_score, "year"),
            **min_max_year_lookup(STUDYearRecord.rank, "rank"),
            **min_max_semester_lookup(1, STUDSemesterRecord.average, "semester_I"),
            **min_max_semester_lookup(2, STUDSemesterRecord.average, "semester_II"),
            **min_max_semester_lookup(1, STUDSemesterRecord.rank, "rank_I"),
            **min_max_semester_lookup(2, STUDSemesterRecord.rank, "rank_II"),
        }
        query = (
            storage.session.query(
                custom_types["year_min"],
                custom_types["year_max"],
                custom_types["semester_I_min"],
                custom_types["semester_I_max"],
                custom_types["semester_II_min"],
                custom_types["semester_II_max"],
                custom_types["rank_min"],
                custom_types["rank_max"],
                custom_types["rank_I_min"],
                custom_types["rank_I_max"],
                custom_types["rank_II_min"],
                custom_types["rank_II_max"],
            )
            .join(User.students)
            .outerjoin(Student.year_records)
            .outerjoin(STUDYearRecord.semester_records)
            .outerjoin(STUDSemesterRecord.semesters)
        )

        result = query.one()
        data_to_serialize = {
            "total_average": {
                "min": result.year_min,
                "max": result.year_max,
            },
            "averageI": {
                "min": result.semester_I_min,
                "max": result.semester_I_min,
            },
            "averageII": {
                "min": result.semester_II_min,
                "max": result.semester_II_min,
            },
            "rank": {
                "min": result.rank_min,
                "max": result.rank_max,
            },
            "rankI": {
                "min": result.rank_I_min,
                "max": result.rank_I_max,
            },
            "rankII": {
                "min": result.rank_II_min,
                "max": result.rank_II_max,
            },
        }

        # Return the serialized data
        schema = StudentAverageSchema()
        result = schema.dump(data_to_serialize)

        return jsonify(**result), 200
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)


@admin.route("/students/grade-counts", methods=["GET"])
@admin_required
def student_grade_counts(admin_data: UserT) -> Tuple[Response, int]:
    """
    Retrieve and return the count of students in each grade.

    Returns:
        Response: A JSON response containing the count of students in each grade.
                  If no students are found, returns a 404 error with an appropriate message.
    """
    query = (
        storage.session.query(
            Grade.grade, func.count(STUDYearRecord.grade_id).label("grade_count")
        )
        .join(STUDYearRecord.grades)
        .group_by(Grade.id)
        .order_by(Grade.grade)
    )
    # Process results
    result = query.all()

    data_to_serialize = [
        {"grade": grade, "total": grade_count} for grade, grade_count in result
    ]

    # Return the serialized data
    schema = StudentGradeCountsSchema(many=True)
    result = schema.dump(data_to_serialize)

    return jsonify(result), 200


@admin.route("/students/section-counts", methods=["GET"])
@admin_required
def student_section_counts(admin_data: UserT) -> Tuple[Response, int]:
    """
    Retrieve and return the count of students in each section.

    Returns:
        Response: A JSON response containing the count of students in each section.
                  If no students are found, returns a 404 error with an appropriate message.
    """
    query = (
        storage.session.query(
            Section.section,
            func.count(case((Semester.name == 1, 1), else_=None)).label("section_I"),
            func.count(case((Semester.name == 2, 1), else_=None)).label("section_II"),
        )
        .join(STUDSemesterRecord.sections)
        .join(STUDSemesterRecord.semesters)
        .group_by(Section.section)
        .order_by(Section.section)
    )
    # Process results
    result = query.all()

    data_to_serialize = [
        {
            "sectionI": {"section": section, "total": section_I},
            "sectionII": {"section": section, "total": section_II},
        }
        for section, section_I, section_II in result
    ]

    # Return the serialized data
    schema = StudentSectionCountsSchema(many=True)
    result = schema.dump(data_to_serialize)

    return jsonify(**result), 200


@admin.route("/students/views", methods=["GET"])
@admin_required
def student_views(admin_data: UserT) -> Tuple[Response, int]:
    """
    Retrieve and return the views of students.

    Returns:
        Response: A JSON response containing the views of students.
                  If no students are found, returns a 404 error with an appropriate message.
    """
    return jsonify(
        [
            {
                "id": uuid.uuid4(),
                "name": "new View",
                "columns": [""],
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
        ]
    ), 200


@admin.route("/teachers", methods=["GET"])
@admin_required
def all_teachers(admin_data: UserT) -> Tuple[Response, int]:
    """
    Retrieve and return a list of teachers with pagination and optional search functionality.

    Args:
        admin_data (dict): Data related to the admin making the request.
    """
    url = request.url
    parsed_url = urlparse(url)
    data = parse_qs(parsed_url.query)

    query = (
        storage.session.query(
            Teacher.id,
            Teacher.first_name.label("firstName"),
            Teacher.last_name.label("lastName"),
            Teacher.email,
            Teacher.no_of_mark_list.label("markList"),
            User.image_path,
        )
        .join(User, User.id == Teacher.id)
        .group_by(Teacher.id)
    )

    if not query:
        return jsonify({"message": "No teachers found"}), 404

    teacher_list = [
        {
            key: url_for("static", filename=value, _external=True)
            if key == "image_path" and value is not None
            else value
            for key, value in q._asdict().items()
        }
        for q in query
    ]

    return jsonify(
        {
            "teachers": teacher_list,
        }
    ), 200
