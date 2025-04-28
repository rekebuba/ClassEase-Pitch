from datetime import datetime
import re
from marshmallow import Schema, ValidationError, post_dump, post_load, pre_load, validates
from sqlalchemy import and_, or_
from models.base_model import BaseModel
from models.table import Table
from models.subject import Subject
from models.user import User
from models.semester import Semester
from models.student import Student
from models.event import Event
from models.grade import Grade
from models.year import Year
from models import storage
import inspect as pyinspect
from sqlalchemy.orm import DeclarativeMeta


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


# Get all model classes dynamically
def get_all_model_classes():
    # Returns dict of {__tablename__: model_class}
    return {
        cls.__tablename__: cls
        for cls in BaseModel.registry._class_registry.values()
        if hasattr(cls, '__tablename__') and cls is not BaseModel
    }


class BaseSchema(Schema):
    """Base schema with global Case conversion."""

    @post_dump
    def convert_to_camel_case(self, data, **kwargs):
        """Convert keys to camelCase when serializing (dumping)."""
        return to_camel(data)

    @pre_load
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
            raise ValidationError("academic year is required")

        # Fetch the year_id from the database
        year = storage.session.query(Year.id).filter_by(
            ethiopian_year=academic_year
        ).first()

        if year is None:
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

    @staticmethod
    def get_grade_detail(**kwargs) -> Grade:
        if kwargs is None:
            raise ValidationError("grade details are required")

        for key, value in kwargs.items():
            if value is None:
                raise ValidationError(f"Grade {key} is required")

        # Fetch the grade details from the database
        grade = storage.session.query(Grade).filter_by(
            **kwargs).first()

        if grade is None:
            raise ValidationError(
                f"No Grade found for grade details: {kwargs}")

        return grade

    @staticmethod
    def get_subject_detail(**kwargs) -> Subject:
        if kwargs is None:
            raise ValidationError("subject details are required")

        for key, value in kwargs.items():
            if value is None:
                raise ValidationError(f"Subject {key} is required")

        # Fetch the subject details from the database
        subject = storage.session.query(Subject).filter_by(
            **kwargs).first()

        if subject is None:
            raise ValidationError(
                f"No Subject found for subject details: {kwargs}")

        return subject

    @staticmethod
    def get_table(table_id):
        if table_id is None:
            raise ValidationError("table_id is required")

        table_name = storage.session.query(Table.name).filter_by(
            id=table_id
        ).first()
        if table_name is None:
            raise ValidationError(f"No Table found for table_id: {table_id}")

        table_models = get_all_model_classes()
        model = table_models.get(table_name[0])
        if model is None:
            raise ValidationError(
                f"No model class found for table name: {table_name}")

        return model

    @staticmethod
    def get_table_id(table):
        if table is None:
            raise ValidationError("table is required")

        # Fetch the table_id from the database
        table_name = table.__tablename__
        table = storage.session.query(Table).filter_by(
            name=table_name
        ).first()

        return table.id if table else None

    @staticmethod
    def filter_data(model, column_name, operator, value):
        """
        Dynamically create a SQLAlchemy filter based on operator.
        """
        column = getattr(model, column_name, None)
        if column is None:
            raise ValueError(
                f"Column '{column_name}' not found on {model.__tablename__}.")

        OPERATOR_MAPPING = {
            "eq": lambda col, val: col == val,
            "neq": lambda col, val: col != val,
            "lt": lambda col, val: col < val,
            "lte": lambda col, val: col <= val,
            "gt": lambda col, val: col > val,
            "gte": lambda col, val: col >= val,
            "iLike": lambda col, val: col.ilike(f"%{val}%"),
            "like": lambda col, val: col.like(f"%{val}%"),
            "in": lambda col, val: col.in_(val if isinstance(val, list) else [val]),
            "not_in": lambda col, val: ~col.in_(val if isinstance(val, list) else [val]),
            "isEmpty": lambda col, _: or_(col.is_(None), col == ""),
            "isNotEmpty": lambda col, _: and_(col.isnot(None), col != ""),
            "isBetween": lambda col, val: col.between(val[0], val[1]) if isinstance(val, (list, tuple)) and len(val) == 2 else ValueError("isBetween expects list/tuple with 2 elements."),
        }

        op_func = OPERATOR_MAPPING.get(operator)
        if not op_func:
            raise ValueError(f"Unsupported operator: {operator}")

        condition = op_func(column, value)
        if isinstance(condition, ValueError):
            raise condition

        return condition
