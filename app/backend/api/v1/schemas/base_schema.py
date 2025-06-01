from datetime import datetime
import re
from typing import Any, Callable, Dict, List, Optional, Type, Union
from marshmallow import (
    Schema,
    ValidationError,
    post_dump,
    pre_load,
)
from sqlalchemy import ColumnElement, UnaryExpression, and_, or_, true
from sqlalchemy.orm.attributes import InstrumentedAttribute
from api.v1.schemas.config_schema import (
    OPERATOR_MAPPING,
    get_all_model_classes,
    to_camel,
    to_snake,
    to_snake_case_key,
)
from api.v1.utils.typing import RangeDict
from models.base_model import Base
from models.stud_year_record import STUDYearRecord
from models.table import Table
from models.subject import Subject
from models.user import User
from models.semester import Semester
from models.student import Student
from models.event import Event
from models.grade import Grade
from models.year import Year
from models import storage


class BaseSchema(Schema):
    """Base schema with global Case conversion."""

    @post_dump
    def convert_to_camel_case(self, data: Any, **kwargs: Any) -> Any:
        """Convert keys to camelCase when serializing (dumping)."""
        return to_camel(data)

    @pre_load
    def convert_to_snake_case(self, data: Any, **kwargs: Any) -> Any:
        """Convert keys to snake_case when deserializing (loading)."""
        return to_snake(data)

    @staticmethod
    def validate_phone(value: str) -> None:
        """Validate phone number format."""
        pattern = (
            r"^\+?[0-9]{1,3}[-.\s]?\(?[0-9]{1,4}\)?[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,9}$"
        )

        # Check if the phone number matches the pattern
        if not re.match(pattern, value):
            raise ValidationError("Invalid phone number format.")

    @staticmethod
    def is_student_registered(student_id: Optional[str]) -> bool:
        """Check if the student is registered. returns True if registered."""
        if student_id is None:
            raise ValidationError("student id is required")

        is_registered: bool = (
            storage.session.query(Student.is_registered)
            .filter(Student.id == student_id)
            .scalar()
        )

        return is_registered

    @staticmethod
    def generate_section(grade_id: Optional[str], semester_id: Optional[str]) -> None:
        pass  # TODO: new sections to generate

    @staticmethod
    def get_user_id(user_identification: Optional[str]) -> str:
        """Get the user_id based on the user_identification."""
        if user_identification is None:
            raise ValidationError("user is required")

        # Fetch the user_id from the database
        user_id: Optional[str] = (
            storage.session.query(User.id)
            .filter_by(identification=user_identification)
            .scalar()
        )

        if user_id is None:
            raise ValidationError(f"No User found for user: {user_identification}")

        return user_id

    @staticmethod
    def get_year_id(academic_year: Optional[str]) -> str:
        """Get the year_id based on the academic_year."""
        if academic_year is None:
            raise ValidationError("academic year is required")

        # Fetch the year_id from the database
        year_id: Optional[str] = (
            storage.session.query(Year.id)
            .filter_by(ethiopian_year=academic_year)
            .scalar()
        )

        if year_id is None:
            raise ValidationError(f"No Year found for academic_year: {academic_year}")

        return year_id

    @staticmethod
    def get_grade_id(grade_name: Optional[str]) -> str:
        """Get the grade_id based on the grade_name."""
        if grade_name is None:
            raise ValidationError("grade is required")

        # Fetch the grade_id from the database
        grade_id: Optional[str] = (
            storage.session.query(Grade.id).filter_by(grade=grade_name).scalar()
        )

        if grade_id is None:
            raise ValidationError(f"No Grade found for grade: {grade_id}")

        return grade_id

    @staticmethod
    def get_student_year_records_id(year_id: Optional[str]) -> str:
        """Get the student_year_records_id based on the year_id."""
        if year_id is None:
            raise ValidationError("year_id is required")

        # Fetch the year_records_id from the database
        year_record_id: Optional[str] = (
            storage.session.query(STUDYearRecord.id).filter_by(year_id=year_id).scalar()
        )

        if year_record_id is None:
            raise ValidationError(f"No Year Records found for year_id: {year_id}")

        return year_record_id

    @staticmethod
    def get_semester_id(
        semester_name: Optional[str], academic_year: Optional[str]
    ) -> str:
        if semester_name is None:
            raise ValidationError("semester is required")
        if academic_year is None:
            raise ValidationError("academic year is required")

        # Fetch the semester_id from the database
        semester = storage.session.query(Semester).all()
        semester_id: Optional[str] = (
            storage.session.query(Semester.id)
            .join(Event, Semester.event_id == Event.id)  # Fix join condition
            .join(Year, Event.year_id == Year.id)
            .filter(
                Semester.name == semester_name,
                Year.ethiopian_year == academic_year,
            )
            .scalar()
        )

        if semester_id is None:
            raise ValidationError(
                f"No Semester found for academic_year: {academic_year}"
            )

        return semester_id

    @staticmethod
    def get_subject_id(
        subject_name: Optional[str],
        subject_code: Optional[str],
        grade_id: Optional[str],
    ) -> str:
        if subject_name is None:
            raise ValidationError("subject name is required")
        if subject_code is None:
            raise ValidationError("subject code is required")
        if grade_id is None:
            raise ValidationError("grade_id is required")

        # Fetch the subject_id from the database
        subject_id: Optional[str] = (
            storage.session.query(Subject.id)
            .filter_by(name=subject_name, code=subject_code, grade_id=grade_id)
            .scalar()
        )

        if subject_id is None:
            raise ValidationError(f"No Subject found for subject_code: {subject_code}")

        return subject_id

    @staticmethod
    def get_grade_detail(**kwargs: Any) -> Grade:
        if kwargs is None:
            raise ValidationError("grade details are required")

        for key, value in kwargs.items():
            if value is None:
                raise ValidationError(f"Grade {key} is required")

        # Fetch the grade details from the database
        grade = storage.session.query(Grade).filter_by(**kwargs).first()

        if grade is None:
            raise ValidationError(f"No Grade found for grade details: {kwargs}")

        return grade

    @staticmethod
    def get_subject_detail(**kwargs: Any) -> Subject:
        if kwargs is None:
            raise ValidationError("subject details are required")

        for key, value in kwargs.items():
            if value is None:
                raise ValidationError(f"Subject {key} is required")

        # Fetch the subject details from the database
        subject = storage.session.query(Subject).filter_by(**kwargs).first()

        if subject is None:
            raise ValidationError(f"No Subject found for subject details: {kwargs}")

        return subject

    @staticmethod
    def get_table(table_id: Optional[str]) -> Type[Base]:
        if table_id is None:
            raise ValidationError("table_id is required")

        table_name: Optional[str] = (
            storage.session.query(Table.name).filter_by(id=table_id).scalar()
        )
        if table_name is None:
            raise ValidationError(f"No Table found for table_id: {table_id}")

        table_models = get_all_model_classes()
        model = table_models.get(table_name)
        if model is None:
            raise ValidationError(f"No model class found for table name: {table_name}")

        return model

    @staticmethod
    def get_table_id(table: Optional[Union[Base, Type[Base]]]) -> str | None:
        if table is None:
            raise ValidationError("table is required")

        # Fetch the table_id from the database
        table_name = table.__tablename__
        table_id = storage.session.query(Table.id).filter_by(name=table_name).scalar()

        return table_id if table_id else None

    @staticmethod
    def update_list_value(
        value: Any, model: Type[Base], column_name: Union[List[str], str]
    ) -> Any:
        """
        Update the list value to match the model's column type.
        """
        if value is None:
            return None
        col_name = column_name if isinstance(column_name, str) else column_name[0]

        # Find the column and get its Python type
        column_obj = next(
            (col for col in model.__table__.columns if col.name == col_name), None
        )
        if column_obj is None:
            raise ValidationError(
                f"Column '{col_name}' not found on {model.__tablename__}."
            )

        try:
            expected_type = column_obj.type.python_type
        except NotImplementedError:
            raise ValidationError(f"Unsupported type for column '{col_name}'.")

        # Type conversion logic
        converters: Dict[Type[Any], Callable[[Any], Any]] = {
            str: lambda v: str(v),
            int: lambda v: int(v),
            float: lambda v: float(v),
            bool: lambda v: bool(v),
            datetime: lambda v: datetime.fromisoformat(v) if isinstance(v, str) else v,
        }

        converter = converters.get(expected_type)
        if converter is None:
            raise ValueError(f"No converter available for type: {expected_type}")

        try:
            return (
                [converter(item) for item in value if item is not None]
                if isinstance(value, list)
                else converter(value)
            )
        except Exception:
            raise ValidationError(f"Failed to convert values for column '{col_name}'")

    @staticmethod
    def filter_multiple_columns(
        model: Type[Base],
        column_name: List[str],
        operator: str,
        value: str,
    ) -> List[ColumnElement[Any]]:
        """
        Filter multiple columns based on the operator and value.
        """
        result: List[ColumnElement[Any]] = []
        if not column_name:
            return result

        # Validate operator early
        if operator not in OPERATOR_MAPPING:
            raise ValueError(f"Unsupported operator: {operator}")

        # Tokenize input value
        tokens = value.split()
        if not tokens:
            return []

        # Reverse tokens for endWith operator
        if operator == "endWith":
            tokens = tokens[::-1]
            column_name = column_name[::-1]

        if operator in {"iLike", "notLike"}:
            for col_name in column_name:
                for token in tokens:
                    condition = BaseSchema.build_operator_condition(
                        model, col_name, operator, token
                    )

                    if condition is not None:
                        result.append(condition)

            if operator == "notLike":
                # Combine conditions with and for notLike
                return [and_(*result)] if result else []

            return [or_(*result)] if result else []

        else:
            for token, col_name in zip(tokens, column_name):
                condition = BaseSchema.build_operator_condition(
                    model, col_name, operator, token
                )

                if condition is not None:
                    result.append(condition)

            # Combine conditions with and for eq/ne
            return [and_(*result)] if result else []

    @staticmethod
    def build_operator_condition(
        model: Type[Base],
        column_name: str,
        operator: str,
        token: Any,
    ) -> Optional[ColumnElement[Any]]:
        col = getattr(model, column_name, None)
        if col is None:
            raise ValidationError(
                f"Column '{column_name}' not found on {model.__tablename__}."
            )

        op_func = OPERATOR_MAPPING.get(operator)
        if not callable(op_func):
            raise ValidationError(
                f"Operator '{operator}' is not callable or not defined."
            )
        try:
            return op_func(col, token)
        except Exception as e:
            raise ValidationError(f"Invalid value for operator '{operator}': {e}")

    @staticmethod
    def filter_data(
        model: Type[Base],
        column_name: Union[str, List[str]],
        operator: Optional[str],
        value: Any,
        range: Optional[RangeDict] = None,
    ) -> List[ColumnElement[Any]]:
        """
        Dynamically create a SQLAlchemy filter based on operator.
        """
        result: List[ColumnElement[Any]] = []
        if isinstance(column_name, list) and operator and isinstance(value, str):
            return BaseSchema.filter_multiple_columns(
                model, column_name, operator, value
            )
        elif isinstance(column_name, str) and operator:
            condition = BaseSchema.build_operator_condition(
                model, column_name, operator, value
            )
        if condition is not None:
            result.append(condition)

        return result

    @staticmethod
    def sort_data(
        model: Type[Base], column_name: Union[str, List[str]], order: bool
    ) -> list[UnaryExpression[Any]]:
        """
        Dynamically create a SQLAlchemy sort based on order.
        """
        if isinstance(column_name, list):
            return BaseSchema.sort_multiple_columns(model, column_name, order)

        col: Optional[InstrumentedAttribute[Any]] = getattr(model, column_name, None)
        if col is None:
            raise ValidationError(
                f"Column '{column_name}' not found on {model.__tablename__}."
            )

        if order:
            return [col.desc()]
        elif not order:
            return [col.asc()]
        else:
            raise ValidationError(f"Unsupported sort order: {order}")

    @staticmethod
    def sort_multiple_columns(
        model: Type[Base], column_names: List[str], order: bool
    ) -> list[UnaryExpression[Any]]:
        """
        Sort multiple columns based on the order.
        """
        result: List[UnaryExpression[Any]] = []
        for column in column_names:
            col: Optional[InstrumentedAttribute[Any]] = getattr(model, column, None)
            if col is None:
                raise ValidationError(
                    f"Column '{column}' not found on {model.__tablename__}."
                )

            if order:
                result.append(col.desc())
            elif not order:
                result.append(col.asc())
            else:
                raise ValidationError(f"Unsupported sort order: {order}")

        return result
