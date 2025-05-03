from datetime import datetime
import re
from marshmallow import Schema, ValidationError, post_dump, post_load, pre_load, validates
from sqlalchemy import and_, or_
from api.v1.schemas.config_schema import *
from models.stud_year_record import STUDYearRecord
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
                   .filter(Student.id == student_id)
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
            grade=grade_name
        ).first()

        if grade.id is None:
            raise ValidationError(f"No Grade found for grade: {grade}")

        return grade.id

    @staticmethod
    def get_student_year_records_id(year_id):
        if year_id is None:
            raise ValidationError("year_id is required")

        # Fetch the year_records_id from the database
        year_records = storage.session.query(STUDYearRecord.id).filter_by(
            year_id=year_id
        ).first()

        if year_records is None:
            raise ValidationError(
                f"No Year Records found for year_id: {year_id}")

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
    def update_list_value(value: list[str | int], model, column_name: str) -> list:
        """
        Update the list value to match the model's column type.
        """
        if not isinstance(value, list):
            raise ValidationError(
                f"Expected a list for {column_name}, got {type(value)}")

        col_name = column_name
        # Find the column and get its Python type
        column_obj = next(
            (col for col in model.__table__.columns if col.name == col_name), None)
        if column_obj is None:
            raise ValidationError(
                f"Column '{col_name}' not found on {model.__tablename__}.")

        try:
            expected_type = column_obj.type.python_type
        except NotImplementedError:
            raise ValidationError(
                f"Unsupported type for column '{column_name}'.")

        # Type conversion logic
        converters = {
            str: lambda v: str(v),
            int: lambda v: int(v),
            float: lambda v: float(v),
            bool: lambda v: bool(v),
            datetime: lambda v: datetime.fromisoformat(
                v) if isinstance(v, str) else v
        }

        if expected_type not in converters:
            raise ValidationError(
                f"No conversion rule for type '{expected_type}' on column '{column_name}'.")

        try:
            return [converters[expected_type](item) for item in value]
        except Exception as e:
            raise ValueError(
                f"Failed to convert values for column '{column_name}': {e}")

    @staticmethod
    def filter_data(model, column_name: str | list[str], operator, value, range):
        """
        Dynamically create a SQLAlchemy filter based on operator.
        """
        columns = column_name if isinstance(
            column_name, list) else [column_name]
        result = []

        for column in columns:
            col_name = to_snake_case_key(column)
            col = getattr(model, col_name, None)
            if col is None:
                raise ValidationError(
                    f"Column '{col_name}' not found on {model.__tablename__}.")

            condition = None  # Initialize condition to ensure type is defined

            if operator is not None or value is not None:
                op_func = OPERATOR_MAPPING.get(operator)
                if not callable(op_func):
                    raise ValidationError(
                        f"Operator '{operator}' is not callable or not defined.")

                try:
                    condition = op_func(col, value)
                except Exception as e:
                    raise ValidationError(
                        f"Invalid value for operator '{operator}': {e}")
            elif range is not None:
                op_func = OPERATOR_MAPPING.get("isBetween")
                if not callable(op_func):
                    raise ValidationError(
                        f"Operator '{operator}' is not callable or not defined.")

                condition = op_func(col, range['min'], range['max'])

            if condition is not None:
                result.append(condition)

        if len(result) > 1:
            # Combine conditions with or if multiple filters are applied
            return [or_(*result)]

        return result

    @staticmethod
    def sort_data(model, column_name: str | list[str], order: bool) -> list:
        """
        Dynamically create a SQLAlchemy sort based on order.
        """
        columns = [column for column in column_name] if isinstance(
            column_name, list) else [column_name]
        result = []
        for column in columns:
            col_name = to_snake_case_key(column)
            col = getattr(model, col_name, None)
            if col is None:
                raise ValidationError(
                    f"Column '{col_name}' not found on {model.__tablename__}.")

            if order == True:
                result.append(col.desc())
            elif order == False:
                result.append(col.asc())
            else:
                raise ValidationError(f"Unsupported sort order: {order}")

        return result
