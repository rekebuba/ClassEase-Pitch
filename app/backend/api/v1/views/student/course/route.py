from datetime import datetime
import random
from typing import Tuple
from flask import Response, jsonify, request
from marshmallow import ValidationError
from sqlalchemy import and_, update
from api.v1.utils.typing import UserT
from api.v1.views.utils import student_required
from api.v1.views.student import stud
from api.v1.views.student.course.schema import CourseListSchema
from models.assessment import Assessment
from models.section import Section
from models.semester import Semester
from models.student import Student
from models.subject import Subject
from models.year import Year
from models.event import Event
from models.grade import Grade
from models.stud_semester_record import STUDSemesterRecord
from models.stud_year_record import STUDYearRecord
from models import storage
from api.v1.views import errors


@stud.route("/course/registration", methods=["GET"])
@student_required
def list_of_course_available(user_data: UserT) -> Tuple[Response, int]:
    """
    Retrieve the course registration status of a student.
    """
    try:
        student_data = (
            storage.session.query(Student).filter_by(user_id=user_data.id).first()
        )
        if not student_data:
            return jsonify({"message": "Student not found"}), 404

        if student_data.is_active:
            return jsonify({"message": "Student is not active"}), 400

        available_semester = (
            storage.session.query(Semester, Event, Year)
            .join(Event, Semester.event_id == Event.id)
            .join(Year, Event.year_id == Year.id)
            .filter(
                Semester.name
                == (
                    1
                    if student_data.next_grade_id or not student_data.semester_id
                    else 2
                ),
                Year.ethiopian_year
                == (Year.ethiopian_year + (1 if student_data.next_grade_id else 0)),
                Event.registration_start <= datetime.now().date(),
                Event.registration_end >= datetime.now().date(),
            )
            .first()
        )
        if not available_semester:
            return jsonify({"message": "Registration is closed"}), 400

        # Query subjects based on student's next grade
        subjects = (
            storage.session.query(Subject)
            .join(Grade, Grade.id == Subject.grade_id)
            .filter(
                Grade.id
                == (student_data.next_grade_id or student_data.current_grade_id)
            )
            .all()
        )

        schema = CourseListSchema()
        result = schema.dump(
            {
                "courses": [subject.to_dict() for subject in subjects],
                "semester": available_semester[0].name,
                "academic_year": available_semester[2].ethiopian_year,
                "grade": storage.session.query(Grade.grade)
                .filter_by(
                    id=student_data.next_grade_id or student_data.current_grade_id
                )
                .scalar(),
            }
        )

        return jsonify(result), 200
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)


@stud.route("/course/registration", methods=["POST"])
@student_required
def register_course(user_data: UserT) -> Tuple[Response, int]:
    try:
        data = request.get_json()
        if not data:
            raise ValidationError("Not a JSON")
        student_data = (
            storage.session.query(Student).filter_by(user_id=user_data.id).first()
        )
        if not student_data:
            return jsonify({"message": "Student not found"}), 404

        data = {**data, "student_id": student_data.id}

        course_schema = CourseListSchema()
        valid_data = course_schema.load(data)

        if valid_data.get("semester") == 1:
            year_record = STUDYearRecord(
                student_id=valid_data.get("student_id"),
                grade_id=valid_data.get("grade_id"),
                year_id=valid_data.get("year_id"),
            )
            storage.add(year_record)
            storage.session.flush()
        else:
            year_record = (
                storage.session.query(STUDYearRecord)
                .filter_by(
                    student_id=valid_data.get("student_id"),
                    grade_id=valid_data.get("grade_id"),
                    year_id=valid_data.get("year_id"),
                )
                .first()
            )

        # random section of ['A', 'B', 'C', 'D']
        random_section = random.choice(["A", "B"])
        section = (
            storage.session.query(Section)
            .join(Section.semester_records)
            .filter(
                and_(
                    Section.grade_id == valid_data.get("grade_id"),
                    Section.section == random_section,
                )
            )
        ).first()

        if section is None:
            section = Section(
                grade_id=valid_data.get("grade_id"),
                section=random_section,
            )
            storage.session.add(section)
            storage.session.flush()

        new_semester_record = STUDSemesterRecord(
            section_id=section.id,
            student_id=valid_data.get("student_id"),
            semester_id=valid_data.get("semester_id"),
        )

        # Associate via relationship (automatically sets year_record_id)
        year_record.semester_records.append(new_semester_record)
        storage.session.flush()

        new_assessment = []
        for form in valid_data["courses"]:
            new_assessment.append(
                Assessment(
                    student_id=valid_data.get("student_id"),
                    subject_id=form.get("subject_id"),
                    semester_record_id=new_semester_record.id,
                )
            )
        storage.session.bulk_save_objects(new_assessment)

        storage.session.execute(
            update(Student)
            .where(Student.id == valid_data.get("student_id"))
            .values(
                semester_id=valid_data.get("semester_id"),
                current_grade_id=valid_data.get("grade_id"),
                next_grade_id=None,
                has_passed=False,
                is_registered=True,
                is_active=True,
                updated_at=datetime.utcnow(),
            )
        )

        storage.save()

        return jsonify({"message": "Course registration successful!"}), 201
    except ValidationError as e:
        storage.rollback()
        return errors.handle_validation_error(e)
    except Exception as e:
        storage.rollback()
        return errors.handle_internal_error(e)
