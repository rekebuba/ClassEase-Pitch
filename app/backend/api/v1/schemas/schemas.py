import json
from flask import url_for
from marshmallow import Schema, validate, ValidationError, post_dump, post_load, pre_dump, pre_load, validates, validates_schema, fields
from pyethiodate import EthDate
from datetime import datetime
import random
import bcrypt
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from api.v1.schemas.base_schema import BaseSchema
from api.v1.schemas.config_schema import *
from api.v1.schemas.custom_schema import *
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
from models.event import Event
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
    created_at = fields.String(required=False)
    table_id = fields.String(required=False)

    @staticmethod
    def _hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def _generate_id(role):
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
        identification = ''
        section = ''

        # Assign prefix based on role
        if role == CustomTypes.RoleEnum.STUDENT.value:
            section = 'MAS'
        elif role == CustomTypes.RoleEnum.TEACHER.value:
            section = 'MAT'
        elif role == CustomTypes.RoleEnum.ADMIN.value:
            section = 'MAA'
        else:
            raise ValidationError('Invalid Role')

        unique = True
        while unique:
            num = random.randint(1000, 9999)
            starting_year = EthDate.date_to_ethiopian(
                datetime.now()).year % 100  # Get last 2 digits of the year
            identification = f'{section}/{num}/{starting_year}'

            # Check if the generated ID already exists in the users table
            if not storage.get_first(User, identification=identification):
                unique = False

        return identification

    @validates_schema
    def validate_data(self, data, **kwargs):
        if data['role'] not in [member.value for member in CustomTypes.RoleEnum]:
            raise ValidationError('Invalid role type.')
        if storage.session.query(User).filter_by(national_id=data['national_id']).first():
            raise ValidationError('User already exists.')

    @pre_load
    def assign_id_and_password(self, data, **kwargs):
        data['identification'] = UserSchema._generate_id(
            data['role'])
        data['password'] = UserSchema._hash_password(
            data['identification'])
        return data

    @post_dump
    def update_fields(self, data, **kwargs):
        # Add the full URL for the image_path if it exists
        if 'image_path' in data and data['image_path'] is not None:
            data['image_path'] = url_for(
                'static', filename=data['image_path'], _external=True)
        data['table_id'] = self.get_table_id(User)

        return data


class AuthSchema(BaseSchema):
    """Schema for validating user authentication data."""
    id = fields.String(required=True, load_only=True)
    password = fields.String(required=True, load_only=True)
    role = fields.String(required=False, dump_only=True)
    api_key = fields.String(dump_only=True)
    message = fields.String(dump_only=True)

    @staticmethod
    def _check_password(stored_password, provided_password):
        """Check if the provided password matches the stored hashed password."""
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

    @validates_schema
    def validate_data(self, data, **kwargs):
        user = storage.session.query(User).filter_by(
            identification=data['id']).first()

        if user is None or not AuthSchema._check_password(user.password, data['password']):
            raise InvalidCredentialsError('Invalid credentials.')

    @post_load
    def load_user(self, data, **kwargs):
        return storage.session.query(User).filter_by(identification=data['id']).first().to_dict()


class AdminSchema(BaseSchema):
    """Admin schema for validating and serializing Admin data."""
    user_id = fields.String(dump_only=True)
    first_name = fields.String(required=True, validate=[
        fields.validate.Length(min=2, max=25)])
    father_name = fields.String(required=True, validate=[
        fields.validate.Length(min=2, max=25)])
    grand_father_name = fields.String(required=True, validate=[
        fields.validate.Length(min=2, max=25)])
    date_of_birth = fields.Date(required=True, format='iso')
    email = fields.Email(required=True)
    gender = fields.String(required=True, validate=[
        fields.validate.OneOf(['M', 'F'])])
    phone = fields.String(required=True)
    address = fields.String(required=True)

    user = fields.Nested(UserSchema)

    @pre_load
    def set_defaults(self, data, **kwargs):
        # add default values
        self.validate_phone(data['phone'])
        if data.get('gender'):
            data['gender'] = data['gender'].upper()

        return data

    @validates_schema
    def validate_data(self, data, **kwargs):
        if storage.session.query(Admin).filter_by(email=data['email']).first():
            raise ValidationError('Email already exists.')

    @validates('phone')
    def validate_teacher_phone(self, value):
        self.validate_phone(value)


class TeacherSchema(BaseSchema):
    """Teacher schema for validating and serializing Teacher data."""
    user_id = fields.String(dump_only=True)
    first_name = fields.String(required=True, validate=[
        fields.validate.Length(min=2, max=25)])
    father_name = fields.String(required=True, validate=[
        fields.validate.Length(min=2, max=25)])
    grand_father_name = fields.String(required=True, validate=[
        fields.validate.Length(min=2, max=25)])
    date_of_birth = fields.Date(required=True, format='iso')
    email = fields.Email(required=True)
    gender = fields.String(required=True, validate=[
        fields.validate.OneOf(['M', 'F'])])
    phone = fields.String(required=True)
    address = fields.String(required=True)
    year_of_experience = fields.Integer(required=True, validate=[
        fields.validate.Range(min=0)])
    qualification = fields.String(required=True)

    user = fields.Nested(UserSchema)

    @pre_load
    def set_defaults(self, data, **kwargs):
        # add default values
        if data.get('gender'):
            data['gender'] = data['gender'].upper()

        return data

    @validates_schema
    def validate_data(self, data, **kwargs):
        if storage.session.query(Teacher).filter_by(email=data['email']).first():
            raise ValidationError('Email already exists.')

    @validates('phone')
    def validate_teacher_phone(self, value):
        self.validate_phone(value)


class StudentNameSchema(BaseSchema):
    """Student name schema for validating and serializing Student data."""
    first_name = fields.String(required=True, validate=[
        fields.validate.Length(min=2, max=25)])
    father_name = fields.String(required=True, validate=[
        fields.validate.Length(min=2, max=25)])
    grand_father_name = fields.String(required=True, validate=[
        fields.validate.Length(min=2, max=25)])

    table_id = fields.String(required=False)


class StudentSchema(BaseSchema):
    """Student schema for validating and serializing Student data."""
    user_id = fields.String(dump_only=True)
    student_name = fields.Nested(StudentNameSchema, required=True)
    guardian_name = fields.String(required=False, validate=[
                                  fields.validate.Length(min=2, max=25)])
    date_of_birth = fields.Date(required=True, format='iso')
    gender = fields.String(required=True, validate=[
                           fields.validate.OneOf(['M', 'F'])])

    father_phone = fields.String(required=False)
    mother_phone = fields.String(required=False)
    guardian_phone = fields.String(required=False)

    academic_year = fields.Integer(required=False, validate=[
        fields.validate.Range(min=2000, max=2100)])
    start_year_id = fields.String(
        required=False, load_default=None, load_only=True)
    current_year_id = fields.String(
        required=False, load_default=None, load_only=True)

    is_transfer = fields.Boolean(required=False)
    previous_school_name = fields.String(required=False, validate=[
        fields.validate.Length(min=2, max=50)], allow_none=True)

    current_grade = fields.Integer(required=False, validate=[
                                   fields.validate.Range(min=1, max=12)])
    current_grade_id = fields.String(required=True)
    next_grade_id = fields.String(required=False)

    semester_id = fields.String(required=False)
    has_passed = fields.Boolean(required=False, load_default=False)
    next_grade = fields.Integer(required=False, validate=[
        fields.validate.Range(min=1, max=12)
    ])
    is_registered = fields.Boolean(required=False)

    birth_certificate = fields.String(required=False)

    has_medical_condition = fields.Boolean(required=False)
    medical_details = fields.String(required=False, validate=[
        fields.validate.Length(min=5, max=500)
    ], allow_none=True)
    has_disability = fields.Boolean(required=False)
    disability_details = fields.String(required=False, validate=[
        fields.validate.Length(min=5, max=500)
    ], allow_none=True)
    requires_special_accommodation = fields.Boolean(required=False)
    special_accommodation_details = fields.String(required=False, validate=[
        fields.validate.Length(min=5, max=500)
    ], allow_none=True)

    is_active = fields.Boolean(required=False, load_default=False)

    user = fields.Nested(UserSchema)

    table_id = fields.String(required=False)

    @pre_load
    def set_defaults(self, data, **kwargs):
        # add default values to the data

        # Convert flat fields into a nested 'student_name' dict
        nested_data = {
            "first_name": data.get("first_name"),
            "father_name": data.get("father_name"),
            "grand_father_name": data.get("grand_father_name"),
        }
        data["student_name"] = nested_data

        year_id = self.get_year_id(data.pop('academic_year'))
        data['current_grade_id'] = self.get_grade_id(data.pop('current_grade'))
        data['start_year_id'] = year_id
        data['current_year_id'] = year_id
        data['gender'] = data.get('gender').upper()

        data['is_transfer'] = data.get('is_transfer') == 'True'
        data['has_disability'] = data.get('has_disability') == 'True'
        data['has_medical_condition'] = data.get(
            'has_medical_condition') == 'True'
        data['requires_special_accommodation'] = data.get(
            'requires_special_accommodation') == 'True'

        if not data.get('is_transfer') and not data.get('previous_school_name', '').strip():
            data['previous_school_name'] = None

        if not data.get('has_medical_condition') and not data.get('medical_details', '').strip():
            data['medical_details'] = None

        if not data.get('has_disability') and not data.get('disability_details', '').strip():
            data['disability_details'] = None

        if not data.get('requires_special_accommodation') and not data.get('special_accommodation_details', '').strip():
            data['special_accommodation_details'] = None

        return data

    @validates_schema
    def validate_data(self, data, **kwargs):
        if not data.get('father_phone') and not data.get('mother_phone'):
            raise ValidationError(
                'Either father_phone or mother_phone must be provided.')
        if data.get('is_transfer') and not data.get('previous_school_name'):
            raise ValidationError(
                'previous_school_name must be provided if is_transfer is True.')
        if data.get('is_transfer') == False and data.get('previous_school_name'):
            raise ValidationError(
                'previous_school_name must be None if is_transfer is False.')
        if data.get('has_medical_condition') and not data.get('medical_details'):
            raise ValidationError(
                'medical_details must be provided if has_medical_condition is True.')
        if data.get('has_medical_condition') == False and data.get('medical_details'):
            raise ValidationError(
                'medical_details must be None if has_medical_condition is False.')
        if data.get('has_disability') and not data.get('disability_details'):
            raise ValidationError(
                'disability_details must be provided if has_disability is True.')
        if data.get('has_disability') == False and data.get('disability_details'):
            raise ValidationError(
                'disability_details must be None if has_disability is False.')
        if data.get('requires_special_accommodation') == True and not data.get('special_accommodation_details'):
            raise ValidationError(
                'special_accommodation_details must be provided if requires_special_accommodation is True.')
        if data.get('requires_special_accommodation') == False and data.get('special_accommodation_details'):
            raise ValidationError(
                'special_accommodation_details must be None if requires_special_accommodation is False.')

    @validates('date_of_birth')
    def validate_date_of_birth(self, value):
        if value > datetime.now().date():
            raise ValidationError('Date of birth cannot be in the future.')

    @validates('father_phone')
    def validate_father_phone(self, value):
        self.validate_phone(value)

    @validates('mother_phone')
    def validate_mother_phone(self, value):
        self.validate_phone(value)

    @validates('guardian_phone')
    def validate_guardian_phone(self, value):
        if value:  # Optional field, only validate if provided
            self.validate_phone(value)

    @validates('semester_id')
    def validate_semester_id(self, value):
        if value:
            semester = storage.get_first(Semester, id=value)
            if not semester:
                raise ValidationError('Invalid semester_id.')

    @pre_dump
    def flatten_to_nested(self, data, **kwargs):
        # Convert flat fields into a nested 'student_name' dict
        nested_data = {
            "first_name": data.get("first_name"),
            "father_name": data.get("father_name"),
            "grand_father_name": data.get("grand_father_name"),
        }
        data["student_name"] = nested_data
        return data

    @post_dump
    def add_fields(self, data, **kwargs):
        data['table_id'] = self.get_table_id(Student)
        return data


class GradeSchema(BaseSchema):
    """Schema for validating grade data."""
    id = fields.String(load_only=True)
    grade = fields.Integer(validate=[fields.validate.Range(min=1, max=12)])

    table_id = fields.String(required=False)

    @post_dump
    def add_fields(self, data, **kwargs):
        data['table_id'] = self.get_table_id(Grade)

        return data


class SemesterCreationSchema(BaseSchema):
    """Schema for validating semester creation data."""
    event_id = fields.String(required=True, load_only=True)
    name = fields.Integer(required=True, load_only=True, validate=[
                          fields.validate.Range(min=1, max=2)])

    @validates('event_id')
    def valid_event_id(self, event_id):
        if not storage.session.query(Event).filter_by(id=event_id).first():
            raise ValidationError('Event Was Not Created Successfully.')


class EventSchema(BaseSchema):
    """Schema for validating event creation data."""
    title = fields.String(required=True, validate=[
                          fields.validate.Length(min=3, max=100)])
    purpose = fields.String(required=True, validate=lambda x: x in [
                            'New Semester', 'Graduation', 'Sports Event', 'Administration', 'Other'])
    organizer = fields.String(required=True, validate=lambda x: x in [
                              'School Administration', 'School', 'Student Club', 'External Organizer'])

    academic_year = fields.Integer(
        validate=[fields.validate.Range(min=2000, max=2100)])

    year_id = fields.String(required=False, load_default=None)

    start_date = fields.Date(required=True, format='iso')
    end_date = fields.Date(required=True, format='iso')
    start_time = fields.DateTime(load_default=None, format='%H:%M:%S')
    end_time = fields.DateTime(load_default=None, format='%H:%M:%S')

    location = fields.String(load_default=None, validate=lambda x: x in [
        'Auditorium', 'Classroom', 'Sports Field', 'Online', 'Other'])
    is_hybrid = fields.Boolean(load_default=False, load_only=True)
    online_link = fields.Url(load_default=None)

    requires_registration = fields.Boolean(load_default=False, load_only=True)
    registration_start = fields.Date(load_default=None, format='iso')
    registration_end = fields.Date(load_default=None, format='iso')

    eligibility = fields.String(load_default=None, validate=lambda x: x in [
                                'All', 'Students Only', 'Faculty Only', 'Invitation Only'])
    has_fee = fields.Boolean(load_default=False)
    fee_amount = fields.Float(load_default=None, validate=[
                              fields.validate.Range(min=0)])

    description = fields.String(load_default=None)

    semester = fields.Nested(
        SemesterCreationSchema,
        load_only=True,
        exclude=("event_id",)
    )

    message = fields.String(dump_only=True)

    @pre_load
    def set_defaults(self, data, **kwargs):
        # add default values to the data
        data['year_id'] = self.get_year_id(data.pop('academic_year', None))

        return data

    @validates_schema
    def validate_dates_and_times(self, data, **kwargs):
        """Ensure start_date is before end_date and start_time is before end_time."""
        try:
            if data["start_date"] and data["end_date"]:
                if data["start_date"] > data["end_date"]:
                    raise ValidationError(
                        "Start date cannot be after end date.", "start_date")
            if data["start_time"] and data["end_time"]:
                if data["start_time"] > data["end_time"]:
                    raise ValidationError(
                        "Start time cannot be after end time.", "start_time")
            if data['registration_start'] and data['registration_end']:
                if data['registration_start'] > data['registration_end']:
                    raise ValidationError(
                        "Registration start date cannot be after registration end date.")
            if data['requires_registration'] and not data['registration_start'] and not data['registration_end']:
                raise ValidationError(
                    "Registration dates are required for events that require registration.")
            if data['has_fee'] and data['fee_amount'] <= 0:
                raise ValidationError(
                    "Fee amount is required for events that have a fee.")
            if data['is_hybrid'] and data['online_link'] is None:
                raise ValidationError(
                    "Online link is required for hybrid events.")
            if data['purpose'] == 'New Semester' and data['organizer'] != 'School Administration':
                raise ValidationError(
                    "New semester events must be organized by the school administration.")
            if data['purpose'] == 'New Semester' and data['location'] != 'Online':
                raise ValidationError(
                    "New semester events must have an online location type.")
            if data['purpose'] == 'New Semester' and not data['has_fee']:
                raise ValidationError("New semester events must have a fee.")
            if data['purpose'] == 'New Semester' and not data['requires_registration']:
                raise ValidationError(
                    "New semester events must require registration.")
            if data['purpose'] == 'New Semester' and data['eligibility'] != 'All':
                raise ValidationError(
                    "New semester events must be open to all.")
            if data['purpose'] == 'New Semester' and data['fee_amount'] == 0.00:
                raise ValidationError("New semester events must have a fee.")
        except TypeError as e:
            raise e

    @post_dump
    def add_academic_year(self, data, **kwargs):
        year = (storage.session.query(
            Year.ethiopian_year, Year.gregorian_year)
            .filter(Year.id == data.get('year_id'))
            .first())
        if year:
            ethiopian_year, gregorian_year = year
            parts = gregorian_year.split("/")
            # to get the last two digits of the year (e.g., 2021/2022 -> 2021/22)
            updated_gregorian_year = f"{parts[0]}/{parts[1][-2:]}"

            data['academic_year'] = f"{ethiopian_year} ({updated_gregorian_year})"

        return data


class SubjectSchema(BaseSchema):
    subject = fields.String(required=False)
    subject_code = fields.String(required=False)
    subject_id = fields.String(required=True, load_only=True)

    grade = fields.Integer(required=False)
    grade_id = fields.String(required=True, load_only=True)

    @pre_load
    def set_defaults(self, data, **kwargs):
        # add default values to the data
        data['grade_id'] = self.get_grade_id(data.pop('grade'))
        data['subject_id'] = self.get_subject_id(
            data.pop('subject'), data.pop('subject_code'), data.get('grade_id'))

        return data

    @pre_dump
    def add_fields(self, data, **kwargs):
        grade_detail = self.get_grade_detail(id=data.get('grade_id'))
        subject_detail = self.get_subject_detail(
            id=data.get('id'), code=data.get('code'))

        data['grade'] = grade_detail.grade
        data['subject'] = subject_detail.name
        data['subject_code'] = subject_detail.code

        return data


class CourseListSchema(BaseSchema):
    """Schema for validating a list of Course objects."""
    courses = fields.List(fields.Nested(SubjectSchema), required=True)
    student_id = fields.String(required=True, load_only=True)

    academic_year = fields.Integer(required=True)
    semester = fields.Integer(required=True)
    semester_id = fields.String(required=True, load_only=True)

    grade = fields.Integer(required=True)
    grade_id = fields.String(required=False, load_only=True)

    year_id = fields.String(required=False, load_only=True)

    section_id = fields.String(required=False, load_only=True)

    is_registered = fields.Boolean(required=False, load_only=True)

    @pre_load
    def set_defaults(self, data, **kwargs):
        # add default values to the data
        data['is_registered'] = self.is_student_registered(
            data.get('student_id'))
        data['grade_id'] = self.get_grade_id(data.get('grade'))
        data['semester_id'] = self.get_semester_id(
            data.get('semester'), data.get('academic_year'))
        data['year_id'] = self.get_year_id(data.get('academic_year'))

        return data

    @validates('is_registered')
    def validate_is_registered(self, value):
        if value:
            raise ValidationError("Student is already registered.")


class MarkListTypeSchema(BaseSchema):
    type = fields.String(required=True)
    percentage = fields.Integer(required=True)


class MarkAssessmentSchema(BaseSchema):
    grade = fields.Integer(required=False)
    grade_id = fields.String(required=True)

    semester_id = fields.String(required=True, load_only=True)
    section_id = fields.String(required=False, load_only=True, allow_none=True)

    subjects = fields.List(fields.Nested(SubjectSchema), required=True)

    assessment_type = fields.List(
        fields.Nested(MarkListTypeSchema), required=True)

    @pre_load
    def set_defaults(self, data, **kwargs):
        # add default values to the data
        data['grade_id'] = self.get_grade_id(data.pop('grade'))
        data['section_id'] = self.generate_section(
            data.get('grade_id'), data.get('semester_id'))
        return data


class CreateMarkListSchema(BaseSchema):
    mark_assessment = fields.List(fields.Nested(
        MarkAssessmentSchema), required=True)

    academic_year = fields.Integer(required=False, load_only=True)
    semester = fields.Integer(required=False, load_only=True)
    semester_id = fields.String(required=True, load_only=True)

    @pre_load
    def set_defaults(self, data, **kwargs):
        # add default values to the data
        data['semester_id'] = self.get_semester_id(
            data.pop('semester'), data.pop('academic_year'))

        # Pass semester_id to each item in mark_assessment
        for item in data.get("mark_assessment", []):
            item["semester_id"] = data["semester_id"]

        return data


class UserDetailSchema(BaseSchema):
    user = fields.Nested(UserSchema)
    detail = fields.Method("get_detail")

    def get_detail(self, obj):
        schema_map = {
            CustomTypes.RoleEnum.ADMIN: AdminSchema(only=('first_name', 'father_name', 'grand_father_name')),
            CustomTypes.RoleEnum.STUDENT: StudentSchema(only=('first_name', 'father_name', 'grand_father_name')),
            CustomTypes.RoleEnum.TEACHER: TeacherSchema(only=('first_name', 'father_name', 'grand_father_name')),
        }

        # `role` is an attribute on the object
        role = CustomTypes.RoleEnum(obj['user'].role)
        schema = schema_map.get(role)

        if schema:
            return schema.dump(obj.get('detail', None))

        return None


class AvailableEventsSchema(BaseSchema):
    events = fields.List(fields.Nested(EventSchema), required=True, exclude=('start_time', 'end_time',
                         'registration_start', 'registration_end', 'fee_amount', 'description', 'message'))


class RegisteredGradesSchema(BaseSchema):
    grades = fields.List(fields.Integer, required=True)


class SortSchema(BaseSchema):
    """Schema for validating sorting parameters."""
    column_name = ColumnField(required=False)
    desc = fields.Boolean(required=False)
    table_id = TableIdField(required=False)
    table = TableField(required=False)

    @pre_load
    def set_defaults(self, data, **kwargs):
        # add default values to the data
        data['column_name'] = data.pop('id', None)
        table_id = data.get('table_id', None)
        if isinstance(table_id, list):
            if not table_id:
                raise ValidationError("table id list cannot be empty")

            first_table_value = table_id[0][1]  # value (uuid)
            if all(v == first_table_value for _, v in table_id):
                data['column_name'] = [k for k, _ in table_id]
                data['table_id'] = first_table_value  # overwrite with string
            else:
                raise ValidationError(
                    "All values in table id must be the same to extract keys."
                )

        if data['table_id'] != '':
            data['table'] = self.get_table(data['table_id'])

        return data


class RangeSchema(BaseSchema):
    """Schema for validating range parameters."""
    min = fields.Float(required=False, missing=None, allow_none=True)
    max = fields.Float(required=False, missing=None, allow_none=True)


class FilterSchema(BaseSchema):
    """Schema for validating filter parameters."""
    column_name = ColumnField(required=False, missing=None, allow_none=True)
    filter_id = fields.String(required=False, missing=None, allow_none=True)
    table_id = TableIdField(required=False, missing=None, allow_none=True)
    table = TableField(required=False, missing=None, allow_none=True)
    range = fields.Nested(RangeSchema, required=False,
                          missing=None, allow_none=True)
    variant = fields.String(validate=lambda x: x in [
                            "text", "number", "multiSelect", "boolean", "dateRange", "range"], required=True)
    operator = fields.String(required=False, missing=None, allow_none=True)
    value = ValueField(required=False, missing=None, allow_none=True)

    @validates_schema
    def validate_value(self, data, **kwargs):
        variant = data.get('variant', None)
        operator = data.get('operator', None)
        value = data.get('value', None)

        if not variant:
            raise ValidationError("Missing variant", field_name="variant")

        if operator is not None and value is not None:
            allowed_operators = OPERATOR_CONFIG.get(variant)
            if not allowed_operators:
                raise ValidationError(
                    f"'{variant}' is not a valid variant.", field_name="variant"
                )

            if operator not in allowed_operators:
                raise ValidationError(
                    f"'{operator}' is not valid for variant '{variant}'",
                    field_name="operator"
                )

            expected_type = VALUE_TYPE_RULES.get(variant)
            if expected_type and not isinstance(value, expected_type):
                raise ValidationError(
                    f"Value must be of type {expected_type} when variant is '{variant}'.", field_name="value"
                )

    @pre_load
    def set_defaults(self, data, **kwargs):
        # add default values to the data
        data['column_name'] = data.pop('id', None)
        value = data.get('value', None)
        table_id = data.get('table_id', None)
        if isinstance(table_id, list):
            if not table_id:
                raise ValidationError("table id list cannot be empty")

            first_table_value = table_id[0][1]  # value (uuid)
            if all(v == first_table_value for _, v in table_id):
                data['column_name'] = [k for k, _ in table_id]
                data['table_id'] = first_table_value  # overwrite with string
            else:
                raise ValidationError(
                    "All values in table id must be the same to extract keys."
                )

        if data['table_id'] != '':
            data['table'] = self.get_table(data['table_id'])

            if value is not None and isinstance(value, list):
                data['value'] = self.update_list_value(
                    value, data['table'], data['column_name'])

        return data


class ParamSchema(BaseSchema):
    """Schema for validating parameters."""
    filter_flag = fields.String(required=False)

    filters = fields.List(fields.Nested(FilterSchema),
                          required=False, missing=None, allow_none=True)
    valid_filters = fields.List(fields.Raw(), required=False)
    custom_filters = fields.List(fields.Raw(), required=False)
    join_operator = JoinOperatorField(required=False)

    page = fields.Integer(required=False, set_defaults=1)
    per_page = fields.Integer(required=False, set_defaults=10)

    sort = fields.List(fields.Nested(SortSchema), required=False)
    valid_sorts = fields.List(fields.Raw(), required=False)
    custom_sorts = fields.List(fields.Raw(), required=False)

    @post_load
    def set_defaults(self, data, **kwargs):
        # add default values to the data
        valid_filters = []
        valid_sorts = []
        custom_sorts = []
        custom_filters = []
        for f_item in data["filters"] if data.get("filters") else []:
            if "table" in f_item and f_item["table"] is not None:
                result = self.filter_data(
                    f_item["table"],
                    f_item['column_name'],
                    f_item["operator"],
                    f_item['value'],
                    f_item['range']
                )
                valid_filters.extend(result)
            else:
                custom_filters.append(f_item)
        data.pop('filters', None)
        data['valid_filters'] = valid_filters

        for s_item in data["sort"] if data.get("sort") else []:
            if "table" in s_item and s_item["table"] is not None:
                result = self.sort_data(
                    s_item["table"],
                    s_item['column_name'],
                    s_item['desc']
                )
                # Adds all items from result to valid_sorts
                valid_sorts.extend(result)
            else:
                custom_sorts.append(s_item)
        data.pop('sort', None)
        data['valid_sorts'] = valid_sorts
        data['custom_filters'] = custom_filters
        data['custom_sorts'] = custom_sorts

        return data


class SectionSchema(BaseSchema):
    id = fields.String(data_key='section_id')
    semester_id = fields.String(required=False)
    semester = fields.Integer(required=False)
    section = fields.String()

    table_id = fields.String(required=False)

    @post_dump
    def add_fields(self, data, **kwargs):
        """Add table_id to the dumped data."""
        data['table_id'] = self.get_table_id(Section)
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
    def add_fields(self, data, **kwargs):
        data['table_id'] = self.get_table_id(STUDYearRecord)

        return data


class AllStudentsSchema(BaseSchema):
    user = fields.Nested(UserSchema(
        only=('identification', 'image_path', 'created_at')))
    # it will be returned as a string ex: "John Doe Smith"
    student = fields.Nested(StudentSchema(
        only=('student_name', 'guardian_name', 'guardian_phone', 'is_active')))
    grade = fields.Nested(GradeSchema(only=('grade',)), required=True)

    sectionI = fields.String(required=False, allow_none=True)
    sectionII = fields.String(required=False, allow_none=True)

    averageI = fields.String(required=False, allow_none=True)
    averageII = fields.String(required=False, allow_none=True)

    rankI = fields.String(required=False, allow_none=True)
    rankII = fields.String(required=False, allow_none=True)

    year_record = fields.Nested(
        STUDYearRecordSchema(only=('final_score', 'rank')))

    @post_dump(pass_many=True)
    def merge_nested(self, data: list, many: bool, **kwargs):
        merged_data = {}

        merged_data['tableId'] = self._extract_table_id(
            data[0] if many else None)
        merged_data['data'] = [self._merge(d) for d in data] if many else [
            self._merge(data)]

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
                    user_table_id = entry.pop('tableId', None)
                    for key in entry:
                        if isinstance(entry[key], dict):
                            table_id[key] = [(k, user_table_id)
                                             for k in entry[key]]
                        else:
                            table_id.setdefault(key, user_table_id)

        return table_id

    def _merge(self, item):
        names = item['student'].pop('studentName')
        full_name = (
            f"{names['firstName']} "
            f"{names['fatherName']} "
            f"{names['grandFatherName']}"
        )
        item["student"]['studentName'] = full_name  # Add as a flat field
        result = {
            **item.pop('user', {}),
            **item.pop('student', {}),
            **item.pop('grade', {}),
            **item.pop('yearRecord', {}),
            **item}
        result.pop("tableId", None)
        return result


class StudentStatusSchema(BaseSchema):
    """Schema for validating student status data."""
    active = fields.Integer(required=True, default=0)
    inactive = fields.Integer(required=True, default=0)
    suspended = fields.Integer(required=True, default=0)
    graduated = fields.Integer(required=False)
    graduated_with_honors = fields.Integer(required=False)


class StudentAverageSchema(BaseSchema):
    """Schema for validating student average data."""
    total_average = fields.Nested(RangeSchema, required=True)
    averageI = fields.Nested(RangeSchema, required=True)
    averageII = fields.Nested(RangeSchema, required=True)
    rank = fields.Nested(RangeSchema, required=True)
    rankI = fields.Nested(RangeSchema, required=True)
    rankII = fields.Nested(RangeSchema, required=True)
