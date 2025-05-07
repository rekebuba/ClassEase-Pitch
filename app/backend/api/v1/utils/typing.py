from typing import Optional, TypeVar, TypedDict
from models.user import User
from models.base_model import Base, CustomTypes

T = TypeVar("T")  # Fully generic

UserT = TypeVar("UserT", bound="User")  # User is your user model class
BaseT = TypeVar("BaseT", bound="Base")


class AuthType(TypedDict):
    """for valid user data."""

    identification: str
    role: CustomTypes.RoleEnum


class PostLoadUser(TypedDict):
    """for user data after post load."""

    id: str
    role: CustomTypes.RoleEnum
    national_id: str
    image_path: Optional[str]
    created_at: Optional[str]
    table_id: Optional[str]
