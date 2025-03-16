from flask import request
from marshmallow import ValidationError
from api.v1.schemas.schemas import AdminSchema, EventCreationSchema, SemesterCreationSchema
from api.v1.services.event_service import EventService
from api.v1.services.semester_service import SemesterService
from models.admin import Admin
from models.user import User
from api.v1.services.user_service import UserService
from models import storage


class AdminService:
    """Service class for Admin model"""
    @staticmethod
    def get_admin_by_user_id(user_id: str) -> Admin:
        return Admin.query.filter_by(user_id=user_id).first()

    @staticmethod
    def get_admin_by_email(email: str) -> Admin | None:
        user = User.query.filter_by(email=email).first()
        if user:
            return Admin.query.filter_by(user_id=user.id).first()
        return None

    @staticmethod
    def update_admin(admin: Admin, **kwargs) -> Admin:
        admin.update(**kwargs)
        return admin

    @staticmethod
    def delete_admin(admin: Admin) -> None:
        admin.delete()
