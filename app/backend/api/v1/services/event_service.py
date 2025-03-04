from flask import request
from marshmallow import ValidationError
from models.admin import Admin
from models.user import User
from api.v1.services.user_service import UserService
from models import storage
from api.v1.schemas.admin.registration_schema import AdminRegistrationSchema
from models import storage
from models.event import Event

class EventService:
    """Service class for Event model"""
    @staticmethod
    def create_event(valid_data) -> Event:
        new_event = Event(**valid_data)
        storage.add(new_event)
        storage.save()
        return new_event
