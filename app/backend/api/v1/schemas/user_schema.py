from datetime import datetime
import random
import bcrypt
from marshmallow import ValidationError, post_load, pre_load, validates_schema, fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from api.v1.schemas.base_schema import BaseSchema
from models.user import User
from werkzeug.datastructures import FileStorage
from models import storage
from pyethiodate import EthDate


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


class UserRegistrationSchema(BaseSchema):
    """Schema for validating user registration data."""
    identification = fields.String(required=False, load_only=True)
    password = fields.String(required=False, load_only=True)
    role = fields.String(required=True)
    national_id = fields.String(required=True)
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
        if role == 'student':
            section = 'MAS'
        elif role == 'teacher':
            section = 'MAT'
        elif role == 'admin':
            section = 'MAA'

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
        if data['role'] not in ['student', 'teacher', 'admin']:
            raise ValidationError('Invalid role type.')
        if storage.session.query(User).filter_by(national_id=data['national_id']).first():
            raise ValidationError('User already exists.')

    @pre_load
    def assign_id_and_password(self, data, **kwargs):
        data['identification'] = UserRegistrationSchema._generate_id(
            data['role'])
        data['password'] = UserRegistrationSchema._hash_password(
            data['identification'])
        return data


class AuthSchema(BaseSchema, Schema):
    """Schema for validating user authentication data."""
    id = fields.String(required=True, load_only=True)
    password = fields.String(required=True, load_only=True)
    role = fields.String(required=False)
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
