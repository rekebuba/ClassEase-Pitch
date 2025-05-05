from typing import TypeVar
from models.user import User
from models.base_model import Base

T = TypeVar("T")  # Fully generic
UserT = TypeVar("UserT", bound="User")  # User is your user model class
BaseT = TypeVar("BaseT", bound="Base")
