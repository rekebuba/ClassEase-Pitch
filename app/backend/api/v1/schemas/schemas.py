from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional, Union
from flask import url_for
from marshmallow import (
    ValidationError,
    post_dump,
    post_load,
    pre_dump,
    pre_load,
    validates,
    validates_schema,
    fields,
)
from pyethiodate import EthDate  # type: ignore
from datetime import datetime
import random
import bcrypt
from api.v1.schemas.base_schema import BaseSchema
from api.v1.schemas.custom_schema import (
    ColumnField,
    FileField,
    FloatOrDateField,
    FormattedDate,
    JoinOperatorField,
    RoleEnumField,
    TableField,
    TableIdField,
    ValueField,
)
from api.v1.schemas.config_schema import OPERATOR_CONFIG, VALUE_TYPE_RULES
from api.v1.utils.typing import AuthType, PostLoadParam, PostLoadUser
from models.section import Section
from models.stud_year_record import STUDYearRecord
from models.grade import Grade
from models.student import Student
from models.base_model import CustomTypes
from models.year import Year
from models import storage
from models.user import User
from models.semester import Semester
from models.teacher import Teacher
from models.admin import Admin


class InvalidCredentialsError(Exception):
    """Exception raised when invalid credentials are provided."""

    pass


class UserSchema(BaseSchema):
    """Schema for validating user registration data."""

    identification = fields.String(required=False)
    password = fields.String(required=False, load_only=True)
    role = RoleEnumField()
    national_id = fields.String(required=True, load_only=True)
    image_path = FileField(required=False, allow_none=True)
    created_at = FormattedDate(required=False)
    table_id = fields.String(required=False)

    @staticmethod
    def _hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def _generate_id(role: CustomTypes.RoleEnum) -> str:
        """
        Generates a custom ID based on the role (Admin, Student, Teacher).

        The ID format is: <section>/<random_number>/<year_suffix>
        - Section: 'MAS' for Student, 'MAT' for Teacher, 'MAA' for Admin
        - Random number: A 4-digit number between 1000 and 9999
        - Year suffix: Last 2 digits of the current Ethiopian year

        Args:
            role (str): The role of the user ('Student', 'Teacher', 'Admin').

        Returns:
            str: A unique custom ID.
        """
        identification = ""
        section = ""

        # Assign prefix based on role
        role_prefix_map: Dict[CustomTypes.RoleEnum, str] = {
            CustomTypes.RoleEnum.STUDENT: "MAS",
            CustomTypes.RoleEnum.TEACHER: "MAT",
            CustomTypes.RoleEnum.ADMIN: "MAA",
        }
        section = role_prefix_map[role]

        unique = True
        while unique:
            num = random.randint(1000, 9999)
            starting_year = (
                EthDate.date_to_ethiopian(datetime.now()).year % 100
            )  # Get last 2 digits of the year
            identification = f"{section}/{num}/{starting_year}"

            # Check if the generated ID already exists in the users table
            if not storage.get_first(User, identification=identification):
                unique = False

        return identification

    @validates_schema
    def validate_data(self, data: Dict[str, Any], **kwargs: Any) -> None:
        print(data)
        if (
            storage.session.query(User.id)
            .filter_by(national_id=data["national_id"])
            .scalar()
        ):
            raise ValidationError("User already exists.")

    @pre_load
    def set_defaults(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        data["identification"] = UserSchema._generate_id(data["role"])
        data["password"] = UserSchema._hash_password(data["identification"])
        return data

    @post_dump
    def update_fields(self, data: PostLoadUser, **kwargs: Any) -> PostLoadUser:
        # Add the full URL for the image_path if it exists
        if "image_path" in data and data["image_path"] is not None:
            data["image_path"] = url_for(
                "static", filename=data["image_path"], _external=True
            )
        data["table_id"] = self.get_table_id(User)

        return data


class FullNameSchema(BaseSchema):
    """Student name schema for validating and serializing Student data."""

    first_name = fields.String(
        required=True, validate=[fields.validate.Length(min=2, max=25)]
    )
    father_name = fields.String(
        required=True, validate=[fields.validate.Length(min=2, max=25)]
    )
    grand_father_name = fields.String(
        required=True, validate=[fields.validate.Length(min=2, max=25)]
    )


class AdminSchema(BaseSchema):
    """Admin schema for validating and serializing Admin data."""

    user_id = fields.String(dump_only=True)
    admin_name = fields.Nested(FullNameSchema, required=True)
    date_of_birth = fields.Date(required=True, format="iso")
    email = fields.Email(required=True)
    gender = fields.String(required=True, validate=[fields.validate.OneOf(["M", "F"])])
    phone = fields.String(required=True)
    address = fields.String(required=True)

    user = fields.Nested(UserSchema)

    @pre_load
    def set_defaults(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        # add default values
        # Convert flat fields into a nested dict
        data["admin_name"] = {
            "first_name": data.pop("first_name", ""),
            "father_name": data.pop("father_name", ""),
            "grand_father_name": data.pop("grand_father_name", ""),
        }

        data["user"] = {
            "national_id": data.pop("national_id", ""),
            "identification": data.pop("identification", ""),
            "role": data.pop("role", ""),
            "image_path": data.pop("image_path", None),
        }

        if data.get("gender"):
            data["gender"] = data["gender"].upper()

        return data

    @post_load
    def merge_data(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        # Merge the nested 'admin_name' dict into the main data dict
        data.update(data.pop("admin_name", {}))

        return data

    @validates_schema
    def validate_data(self, data: Dict[str, Any], **kwargs: Any) -> None:
        if storage.session.query(Admin).filter_by(email=data["email"]).first():
            raise ValidationError("Email already exists.")
        self.validate_phone(data["phone"])

    @pre_dump
    def flatten_to_nested(self, data, **kwargs: Any):
        # Convert flat fields into a nested 'student_name' dict
        nested_data = {
            "first_name": data.get("first_name"),
            "father_name": data.get("father_name"),
            "grand_father_name": data.get("grand_father_name"),
        }
        data["admin_name"] = nested_data
        return data


class TeacherSchema(BaseSchema):
    """Teacher schema for validating and serializing Teacher data."""

    user_id = fields.String(dump_only=True)
    teacher_name = fields.Nested(FullNameSchema, required=True)
    date_of_birth = fields.Date(required=True, format="iso")
    email = fields.Email(required=True)
    gender = fields.String(required=True, validate=[fields.validate.OneOf(["M", "F"])])
    phone = fields.String(required=True)
    address = fields.String(required=True)
    year_of_experience = fields.Integer(
        required=True, validate=[fields.validate.Range(min=0)]
    )
    qualification = fields.String(required=True)

    user = fields.Nested(UserSchema)

    @pre_load
    def set_defaults(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        # add default values
        # Convert flat fields into a nested 'student_name' dict
        data["teacher_name"] = {
            "first_name": data.pop("first_name"),
            "father_name": data.pop("father_name"),
            "grand_father_name": data.pop("grand_father_name"),
        }

        data["user"] = {
            "national_id": data.pop("national_id", ""),
            "identification": data.pop("identification", ""),
            "role": data.pop("role", ""),
            "image_path": data.pop("image_path", None),
        }

        if data.get("gender"):
            data["gender"] = data["gender"].upper()

        return data

    @post_load
    def merge_data(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        # Merge the nested 'teacher_name' dict into the main data dict
        data.update(data.pop("teacher_name", {}))

        return data

    @validates_schema
    def validate_data(self, data: Dict[str, Any], **kwargs: Any) -> None:
        if storage.session.query(Teacher).filter_by(email=data["email"]).first():
            raise ValidationError("Email already exists.")
        self.validate_phone(data["phone"])

    @pre_dump
    def flatten_to_nested(self, data, **kwargs: Any):
        # Convert flat fields into a nested 'student_name' dict
        nested_data = {
            "first_name": data.get("first_name"),
            "father_name": data.get("father_name"),
            "grand_father_name": data.get("grand_father_name"),
        }
        data["teacher_name"] = nested_data
        return data


class StudentSchema(BaseSchema):
    """Student schema for validating and serializing Student data."""

    user_id = fields.String(dump_only=True)
    student_name = fields.Nested(FullNameSchema, required=True)
    guardian_name = fields.String(
        required=False, validate=[fields.validate.Length(min=2, max=25)]
    )
    date_of_birth = fields.Date(required=True, format="iso")
    gender = fields.String(required=True, validate=[fields.validate.OneOf(["M", "F"])])

    father_phone = fields.String(required=False)
    mother_phone = fields.String(required=False)
    guardian_phone = fields.String(required=False)

    academic_year = fields.Integer(
        required=False, validate=[fields.validate.Range(min=2000, max=2100)]
    )
    start_year_id = fields.String(required=False, load_default=None, load_only=True)
    current_year_id = fields.String(required=False, load_default=None, load_only=True)

    is_transfer = fields.Boolean(required=False)
    previous_school_name = fields.String(
        required=False,
        validate=[fields.validate.Length(min=2, max=50)],
        allow_none=True,
    )

    current_grade = fields.Integer(
        required=False, validate=[fields.validate.Range(min=1, max=12)]
    )
    current_grade_id = fields.String(required=True)
    next_grade_id = fields.String(required=False)

    semester_id = fields.String(required=False)
    has_passed = fields.Boolean(required=False, load_default=False)
    next_grade = fields.Integer(
        required=False, validate=[fields.validate.Range(min=1, max=12)]
    )
    is_registered = fields.Boolean(required=False)

    birth_certificate = fields.String(required=False)

    has_medical_condition = fields.Boolean(required=False)
    medical_details = fields.String(
        required=False,
        validate=[fields.validate.Length(min=5, max=500)],
        allow_none=True,
    )
    has_disability = fields.Boolean(required=False)
    disability_details = fields.String(
        required=False,
        validate=[fields.validate.Length(min=5, max=500)],
        allow_none=True,
    )
    requires_special_accommodation = fields.Boolean(required=False)
    special_accommodation_details = fields.String(
        required=False,
        validate=[fields.validate.Length(min=5, max=500)],
        allow_none=True,
    )

    is_active = fields.Boolean(required=False, load_default=False)

    user = fields.Nested(UserSchema)

    table_id = fields.String(required=False)

    @pre_load
    def set_defaults(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        """Normalize and transform input data before validation."""
        data["student_name"] = {
            "first_name": data.pop("first_name", ""),
            "father_name": data.pop("father_name", ""),
            "grand_father_name": data.pop("grand_father_name", ""),
        }

        data["user"] = {
            "national_id": data.pop("national_id", ""),
            "identification": data.pop("identification", ""),
            "role": data.pop("role", ""),
            "image_path": data.pop("image_path", None),
        }

        # Set year and grade IDs
        if "academic_year" in data:
            year_id = self.get_year_id(data.pop("academic_year"))
            data.update({"start_year_id": year_id, "current_year_id": year_id})

        if "current_grade" in data:
            data["current_grade_id"] = self.get_grade_id(data.pop("current_grade"))

        # Normalize gender
        if "gender" in data:
            data["gender"] = data["gender"].upper()

        # Convert string booleans to actual booleans
        bool_fields = [
            "is_transfer",
            "has_disability",
            "has_medical_condition",
            "requires_special_accommodation",
        ]
        for field in bool_fields:
            if field in data and isinstance(data[field], str):
                data[field] = data[field].lower() == "true"

        # Clean empty optional fields
        optional_fields = [
            ("previous_school_name", "is_transfer"),
            ("medical_details", "has_medical_condition"),
            ("disability_details", "has_disability"),
            ("special_accommodation_details", "requires_special_accommodation"),
        ]

        for detail_field, condition_field in optional_fields:
            if not data.get(condition_field) and not data.get(detail_field, "").strip():
                data[detail_field] = None

        return data

    @post_load
    def merge_data(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        # Merge the nested 'student_name' dict into the main data dict
        data.update(data.pop("student_name", {}))

        return data

    @validates_schema
    def validate_data(self, data: Dict[str, Any], **kwargs: Any) -> None:
        # Phone number validation
        if not any([data.get("father_phone"), data.get("mother_phone")]):
            raise ValidationError("At least one parent phone number must be provided")

        # Conditional field validation
        conditions = [
            ("previous_school_name", "is_transfer"),
            ("medical_details", "has_medical_condition"),
            ("disability_details", "has_disability"),
            ("special_accommodation_details", "requires_special_accommodation"),
        ]

        for field, condition in conditions:
            if data.get(condition) and not data.get(field):
                raise ValidationError(
                    f"{field!r} is required when {condition!r} is True"
                )
            if not data.get(condition) and data.get(field):
                raise ValidationError(
                    f"{field!r} must be null when {condition!r} is False"
                )

    @validates("date_of_birth")
    def validate_dob(self, value: datetime, **kwargs: Any) -> None:
        if value > datetime.now().date():
            raise ValidationError("Date of birth cannot be in the future")
        if (datetime.now().date() - value).days < 365 * 5:  # Minimum 5 years old
            raise ValidationError("Student must be at least 5 years old")

    @validates("father_phone")
    def validate_father_phone(self, value: Optional[str], **kwargs: Any) -> None:
        if value:
            self.validate_phone(value)

    @validates("mother_phone")
    def validate_mother_phone(self, value: Optional[str], **kwargs: Any) -> None:
        if value:
            self.validate_phone(value)

    @validates("guardian_phone")
    def validate_guardian_phone(self, value: Optional[str], **kwargs: Any) -> None:
        if value:
            self.validate_phone(value)

    @validates("semester_id")
    def validate_semester_id(self, value: Optional[str], **kwargs: Any) -> None:
        if value and not storage.session.query(Semester).get(value):
            raise ValidationError("Invalid semester_id.")

    @pre_dump
    def flatten_to_nested(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        # Convert flat fields into a nested 'student_name' dict
        data["student_name"] = {
            "first_name": data.pop("first_name", ""),
            "father_name": data.get("father_name", ""),
            "grand_father_name": data.get("grand_father_name", ""),
        }
        return data

    @post_dump
    def add_fields(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        data["table_id"] = self.get_table_id(Student)
        return data


class GradeSchema(BaseSchema):
    """Schema for validating grade data."""

    id = fields.String(load_only=True)
    grade = fields.Integer(validate=[fields.validate.Range(min=1, max=12)])

    table_id = fields.String(required=False)

    @post_dump
    def add_fields(self, data, **kwargs: Any):
        data["table_id"] = self.get_table_id(Grade)

        return data


class SubjectSchema(BaseSchema):
    subject = fields.String(required=False)
    subject_code = fields.String(required=False)
    subject_id = fields.String(required=True, load_only=True)

    grade = fields.Integer(required=False)
    grade_id = fields.String(required=True, load_only=True)

    @pre_load
    def set_defaults(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        # add default values to the data
        data["grade_id"] = self.get_grade_id(data.pop("grade"))
        data["subject_id"] = self.get_subject_id(
            data.pop("subject"), data.pop("subject_code"), data.get("grade_id")
        )

        return data


class UserDetailSchema(BaseSchema):
    user = fields.Nested(UserSchema)
    detail = fields.Method("get_detail")

    def get_detail(self, obj):
        schema_map = {
            CustomTypes.RoleEnum.ADMIN: AdminSchema(only=("admin_name",)),
            CustomTypes.RoleEnum.STUDENT: StudentSchema(only=("student_name",)),
            CustomTypes.RoleEnum.TEACHER: TeacherSchema(only=("teacher_name",)),
        }

        # `role` is an attribute on the object
        role = CustomTypes.RoleEnum(obj["user"].role)
        schema = schema_map.get(role)

        if schema:
            result = schema.dump(obj.get("detail").to_dict())

            nested = next(iter(result.values()), {})
            if isinstance(nested, dict):
                for key, value in nested.items():
                    result[key] = value
                result.pop(next(iter(result)))

            return result

        return None


class RangeSchema(BaseSchema):
    """Schema for validating range parameters."""

    min = FloatOrDateField(required=False, allow_none=True)
    max = FloatOrDateField(required=False, allow_none=True)


class SectionSchema(BaseSchema):
    id = fields.String(data_key="section_id")
    semester_id = fields.String(required=False)
    semester = fields.Integer(required=False)
    section = fields.String()

    table_id = fields.String(required=False)

    @post_dump
    def add_fields(self, data, **kwargs: Any):
        """Add table_id to the dumped data."""
        data["table_id"] = self.get_table_id(Section)
        return data


class STUDYearRecordSchema(BaseSchema):
    user_id = fields.String()
    grade_id = fields.String()

    year = fields.String()
    year_id = fields.String()

    final_score = fields.Float(dump_default=0.0)
    rank = fields.Integer(dump_default=0)

    table_id = fields.String(required=False)

    @post_dump
    def add_fields(self, data, **kwargs: Any):
        data["table_id"] = self.get_table_id(STUDYearRecord)

        return data


class AllStudentsSchema(BaseSchema):
    user = fields.Nested(
        UserSchema(only=("identification", "image_path", "created_at"))
    )
    # it will be returned as a string ex: "John Doe Smith"
    student = fields.Nested(
        StudentSchema(
            only=("student_name", "guardian_name", "guardian_phone", "is_active")
        )
    )
    grade = fields.Nested(GradeSchema(only=("grade",)), required=True)

    sectionI = fields.String(required=False, allow_none=True)
    sectionII = fields.String(required=False, allow_none=True)

    averageI = fields.String(required=False, allow_none=True)
    averageII = fields.String(required=False, allow_none=True)

    rankI = fields.String(required=False, allow_none=True)
    rankII = fields.String(required=False, allow_none=True)

    year_record = fields.Nested(STUDYearRecordSchema(only=("final_score", "rank")))

    @post_dump
    def merge_nested(self, data: list, many: bool, **kwargs: Any):
        merged_data = {}

        merged_data["tableId"] = self._extract_table_id(data[0] if many else None)
        merged_data["data"] = (
            [self._merge(d) for d in data] if many else [self._merge(data)]
        )

        return merged_data

    def _extract_table_id(self, item):
        table_id = {}
        if not item:
            return table_id

        for model in item.keys():
            entries = item[model]
            if not isinstance(entries, list):
                entries = [entries]

            for entry in entries:
                if isinstance(entry, dict):
                    user_table_id = entry.pop("tableId", None)
                    for key in entry:
                        if isinstance(entry[key], dict):
                            table_id[key] = [(k, user_table_id) for k in entry[key]]
                        else:
                            table_id.setdefault(key, user_table_id)

        return table_id

    def _merge(self, item):
        names = item["student"].pop("studentName")
        full_name = (
            f"{names['firstName']} {names['fatherName']} {names['grandFatherName']}"
        )
        item["student"]["studentName"] = full_name  # Add as a flat field
        result = {
            **item.pop("user", {}),
            **item.pop("student", {}),
            **item.pop("grade", {}),
            **item.pop("yearRecord", {}),
            **item,
        }
        result.pop("tableId", None)
        return result
