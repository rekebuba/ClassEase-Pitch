from flask import request
from marshmallow import ValidationError
from models.semester import Semester
from models.admin import Admin
from models.user import User
from api.v1.services.user_service import UserService
from models import storage
from api.v1.schemas.admin.registration_schema import AdminRegistrationSchema
from models import storage


class SemesterService:
    """Service class for Semester model"""
    @staticmethod
    def create_semester(valid_data) -> Semester:
        new_semester = Semester(valid_data)
        storage.add(new_semester)
        storage.save()
        return new_semester
