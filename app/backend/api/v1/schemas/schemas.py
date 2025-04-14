from flask import url_for
from marshmallow import Schema, ValidationError, post_dump, post_load, pre_dump, pre_load, validates, validates_schema, fields
from pyethiodate import EthDate
from datetime import datetime
import random
import bcrypt
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from api.v1.schemas.base_schema import BaseSchema
from werkzeug.datastructures import FileStorage
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


class FileField(fields.Field):
    """Custom field for file validation."""

    def _deserialize(self, value, attr, data, **kwargs):
        if not isinstance(value, FileStorage):
            raise ValidationError("Invalid file type. Expected a file upload.")

        # Validate file size (e.g., 5MB limit)
        if value.content_length > 5 * 1024 * 1024:  # 5MB
            raise ValidationError("File size exceeds the 5MB limit.")

        # Validate file extension (allow only images)
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if not value.filename.lower().endswith(tuple(allowed_extensions)):
            raise ValidationError(
                "Invalid file type. Allowed extensions: png, jpg, jpeg, gif.")

        return value


class RoleEnumField(fields.Field):
    """Custom field for RoleEnum."""

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.value.capitalize()  # Returns "Admin", "Teacher", or "Student"

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            if isinstance(value, CustomTypes.RoleEnum):
                return value
            return CustomTypes.RoleEnum(value)  # Converts string to enum
        except ValueError as error:
            raise ValidationError(
                "Invalid role. Must be one of: admin, teacher, student") from error


class UserSchema(BaseSchema):
    """Schema for validating user registration data."""
    identification = fields.String(required=False)
    password = fields.String(required=False, load_only=True)
    role = RoleEnumField()
    national_id = fields.String(required=True, load_only=True)
    image_path = FileField(required=False, allow_none=True)

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


class StudentSchema(BaseSchema):
    """Student schema for validating and serializing Student data."""
    user_id = fields.String(dump_only=True)
    first_name = fields.String(required=True, validate=[
        fields.validate.Length(min=2, max=25)])
    father_name = fields.String(required=True, validate=[
                                fields.validate.Length(min=2, max=25)])
    grand_father_name = fields.String(required=True, validate=[
                                      fields.validate.Length(min=2, max=25)])
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

    @pre_load
    def set_defaults(self, data, **kwargs):
        # add default values to the data
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

        data['grade'] = grade_detail.name
        data['subject'] = subject_detail.name
        data['subject_code'] = subject_detail.code

        return data


class CourseListSchema(BaseSchema):
    """Schema for validating a list of Course objects."""
    courses = fields.List(fields.Nested(SubjectSchema), required=True)
    student_id = fields.String(required=True, load_only=True)
    user_id = fields.String(required=True, load_only=True)

    academic_year = fields.Integer(required=True)
    semester = fields.Integer(required=True)
    semester_id = fields.String(required=True, load_only=True)

    grade = fields.Integer(required=True)
    grade_id = fields.String(required=False, load_only=True)

    year_record_id = fields.String(required=False, load_only=True)

    section_id = fields.String(required=False, load_only=True)

    is_registered = fields.Boolean(required=False, load_only=True)

    @pre_load
    def set_defaults(self, data, **kwargs):
        # add default values to the data
        data['is_registered'] = self.is_student_registered(
            data.get('student_id'))
        data['user_id'] = self.get_user_id(data.get('student_id'))
        data['grade_id'] = self.get_grade_id(data.get('grade'))
        data['semester_id'] = self.get_semester_id(
            data.get('semester'), data.get('academic_year'))

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
