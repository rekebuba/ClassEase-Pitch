import bcrypt
from flask import request
from marshmallow import ValidationError
from api.v1.schemas.schemas import *
from api.v1.views.methods import save_profile
from api.v1.views.utils import create_token
from models.teacher import Teacher
from models.student import Student
from models.user import User
from models import storage
from models.admin import Admin


class UserService:
    """Base service for user-related operations."""

    def __init__(self):
        pass

    def create_user(self, data):
        user_schema = UserSchema()
        validated_user_data = user_schema.load(data)

        # Save the profile picture if exists
        filepath = None
        if 'image_path' in validated_user_data and validated_user_data['image_path']:
            filepath = save_profile(validated_user_data['image_path'])
            validated_user_data['image_path'] = filepath

        # Create the user
        new_user = User(**validated_user_data)

        return new_user

    def create_role_based_user(self, role, data) -> Admin | None:
        """Create a user with a specific role."""
        # Start a new transaction
        user_data = {
            'role': role,
            'national_id': data.pop('national_id') if 'national_id' in data else None,
            'image_path': request.files.get('image_path')
        }
        # Call the base class method to create a user with role 'admin'
        new_user = self.create_user(user_data)

        storage.add(new_user)
        storage.session.flush()  # Flush to get the new_user.id

        fields = {
            **data,
            'user_id': new_user.id
        }
        if role == 'admin':
            # Validate and create the Admin
            admin_schema = AdminSchema()
            validated_admin_data = admin_schema.load(fields)

            new_admin = Admin(**validated_admin_data)

            storage.add(new_admin)
            storage.save()
            return new_admin
        elif role == 'student':
            student_schema = StudentSchema()

            validated_student_data = student_schema.load(fields)
            new_student = Student(**validated_student_data)

            storage.add(new_student)
            storage.save()
            return new_student
        elif role == 'teacher':
            teacher_schema = TeacherSchema()

            validated_teacher_data = teacher_schema.load(fields)
            new_teacher = Teacher(**validated_teacher_data)

            storage.add(new_teacher)
            storage.save()
            return new_teacher

        return None

    @staticmethod
    def get_user_by_id(user_id):
        return storage.session.query(User).get(user_id).to_dict()

    @staticmethod
    def get_user_by_national_id(national_id):
        return storage.session.query(User).filter_by(national_id=national_id).first().to_dict()

    @staticmethod
    def get_user_by_email(email):
        return storage.session.query(User).filter_by(email=email).first().to_dict()

    @staticmethod
    def generate_api_key(role, user_id):
        """Generate an api_key token based on the user's role"""
        return create_token(user_id, role)
