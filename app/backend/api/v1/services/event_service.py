from flask import request
from marshmallow import ValidationError
from models.admin import Admin
from models.user import User
from api.v1.services.user_service import UserService
from models import storage
from api.v1.schemas.schemas import AdminSchema
from models import storage
from models.event import Event


class EventService:
    """Service class for Event model"""

    @staticmethod
    def create_event(**kwarg) -> Event:
        return Event(**kwarg)
