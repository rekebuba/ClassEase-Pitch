from api.v1.views.methods import save_profile
from api.v1.views.shared.registration.schema import (
    AdminSchema,
    StudentSchema,
    TeacherRegistrationSchema,
)
from extension.enums.enum import RoleEnum
from models import storage
from typing import Any, Dict, Tuple, Type, Union
from marshmallow import Schema
from werkzeug.datastructures import FileStorage
from models.admin import Admin

from models.student import Student
from models.teacher import Teacher
from models.user import User


def create_user(data: Dict[str, Any]) -> User:
    # Save the profile picture if exists
    filepath = None
    if "image_path" in data and isinstance(data["image_path"], FileStorage):
        filepath = save_profile(data["image_path"])
        data["image_path"] = filepath

    # Create the user
    new_user = User(**data)

    storage.add(new_user)
    storage.session.flush()  # Flush to get the new_user.id

    return new_user


def create_role_based_user(
    role_enum: RoleEnum, data: Dict[str, Any]
) -> User | None:
    role_mapping: Dict[
        RoleEnum,
        Tuple[Type[Schema], Union[Type[Admin], Type[Student], Type[Teacher]]],
    ] = {
        RoleEnum.ADMIN: (AdminSchema, Admin),
        RoleEnum.STUDENT: (StudentSchema, Student),
        RoleEnum.TEACHER: (TeacherRegistrationSchema, Teacher),
    }

    if role_enum in role_mapping:
        schema_class, model_class = role_mapping[role_enum]
        schema = schema_class()
        validated_data = schema.load(data)

        new_user = create_user(validated_data.pop("user"))

        new_instance = model_class(user_id=new_user.id, **validated_data)
        storage.add(new_instance)
        storage.save()
        return new_user

    return None
