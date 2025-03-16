from datetime import datetime
import re
from marshmallow import Schema, ValidationError, post_dump, post_load, validates
from models.subject import Subject
from models.user import User
from models.semester import Semester
from models.student import Student
from models.event import Event
from models.grade import Grade
from models.year import Year
from models import storage


def to_snake(data):
    if isinstance(data, dict):
        return {to_snake_case_key(k): to_snake(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [to_snake(item) for item in data]
    else:
        return data


def to_camel(data):
    if isinstance(data, dict):
        return {to_camel_case_key(k): to_camel(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [to_camel(item) for item in data]
    else:
        return data


def to_snake_case_key(s):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()


def to_camel_case_key(s):
    parts = s.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])


class BaseSchema(Schema):
    """Base schema with global Case conversion."""

    @post_dump
    def convert_to_camel_case(self, data, **kwargs):
        """Convert keys to camelCase when serializing (dumping)."""
        return to_camel(data)

    @post_load
    def convert_to_snake_case(self, data, **kwargs):
        """Convert keys to snake_case when deserializing (loading)."""
        return to_snake(data)

    @staticmethod
    def validate_phone(value):
        pattern = r'^\+?[0-9]{1,3}[-.\s]?\(?[0-9]{1,4}\)?[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,9}$'

        # Check if the phone number matches the pattern
        if not re.match(pattern, value):
            raise ValidationError("Invalid phone number format.")

    @staticmethod
    def is_student_registered(student_id):
        if student_id is None:
            raise ValidationError("student id is required")

        # Check if the student is already registered
        student = (storage.session.query(Student)
                   .join(User, User.id == Student.user_id)
                   .filter(User.identification == student_id)
                   .first()
                   )

        if student is None or student.id is None:
            raise ValidationError(
                f"No Student found for student_id: {student_id}")

        return student.is_registered

    @staticmethod
    def generate_section(grade_id, semester_id):
        pass  # TODO: new sections to generate

    @staticmethod
    def get_user_id(user_identification):
        if user_identification is None:
            raise ValidationError("user is required")

        # Fetch the user_id from the database
        user = storage.session.query(User.id).filter_by(
            identification=user_identification
        ).first()

        if user.id is None:
            raise ValidationError(
                f"No User found for user: {user_identification}")

        return user.id

    @staticmethod
    def get_year_id(academic_year):
        if academic_year is None:
            raise ValidationError("academic_year is required")

        # Fetch the year_id from the database
        year = storage.session.query(Year.id).filter_by(
            ethiopian_year=academic_year
        ).first()

        if year.id is None:
            raise ValidationError(
                f"No Year found for academic_year: {academic_year}")

        return year.id

    @staticmethod
    def get_grade_id(grade_name):
        if grade_name is None:
            raise ValidationError("grade is required")

        # Fetch the grade_id from the database
        grade = storage.session.query(Grade.id).filter_by(
            name=grade_name
        ).first()

        if grade.id is None:
            raise ValidationError(f"No Grade found for grade: {grade}")

        return grade.id

    @staticmethod
    def get_year_records_id(user_id, academic_year):
        if academic_year is None:
            raise ValidationError("academic_year is required")

        # Fetch the year_records_id from the database
        year_records = storage.session.query(Year.id).filter_by(
            ethiopian_year=academic_year
        ).first()

        if year_records.id is None:
            raise ValidationError(
                f"No Year Records found for academic_year: {academic_year}")

        return year_records.id

    @staticmethod
    def get_semester_id(semester_name, academic_year):
        if semester_name is None:
            raise ValidationError("semester is required")
        if academic_year is None:
            raise ValidationError("academic year is required")

        # Fetch the semester_id from the database
        semester = (
            storage.session.query(Semester.id)
            .join(Event, Semester.event_id == Event.id)  # Fix join condition
            .join(Year, Event.year_id == Year.id)
            .filter(
                Semester.name == semester_name,
                Year.ethiopian_year == academic_year,
            )
            .first()
        )

        if semester.id is None:
            raise ValidationError(
                f"No Semester found for academic_year: {academic_year}")

        return semester.id

    @staticmethod
    def get_subject_id(subject_name, subject_code, grade_id):
        if subject_name is None:
            raise ValidationError("subject name is required")
        if subject_code is None:
            raise ValidationError("subject code is required")
        if grade_id is None:
            raise ValidationError("grade_id is required")

        # Fetch the subject_id from the database
        subject = storage.session.query(Subject.id).filter_by(
            name=subject_name,
            code=subject_code,
            grade_id=grade_id
        ).first()

        if subject is None or subject.id is None:
            raise ValidationError(
                f"No Subject found for subject_code: {subject_code}")

        return subject.id
