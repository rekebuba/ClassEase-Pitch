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

        # Save the profile picture if exists
        filepath = None
        if 'image_path' in data and data['image_path']:
            filepath = save_profile(data['image_path'])
            data['image_path'] = filepath

        # Create the user
        new_user = User(**data)

        storage.add(new_user)
        storage.session.flush()  # Flush to get the new_user.id

        return new_user

    def create_role_based_user(self, role, data) -> Admin | Student | Teacher | None:
        role_mapping = {
            CustomTypes.RoleEnum.ADMIN: (AdminSchema, Admin),
            CustomTypes.RoleEnum.STUDENT: (StudentSchema, Student),
            CustomTypes.RoleEnum.TEACHER: (TeacherSchema, Teacher),
        }
        # Convert role (string) to the corresponding Enum value
        try:
            role_enum = CustomTypes.RoleEnum(role)
        except ValueError:
            raise ValidationError("Invalid role")

        if role_enum in role_mapping:
            schema_class, model_class = role_mapping[role_enum]
            schema = schema_class()
            validated_data = schema.load(data)

            user = validated_data.pop("user")
            self.create_user(user)

            new_instance = model_class(**validated_data)
            storage.add(new_instance)
            storage.save()
            return new_instance

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
