#!/usr/bin/python

from typing import Any, Callable, Dict, Iterator, List, Optional, Type
from flask.testing import FlaskClient
import pytest
from tests.test_api.factories import (
    AdminFactory,
    StudentFactory,
    TeacherFactory,
    UserFactory,
)
import os
from models.base_model import CustomTypes
from sqlalchemy.orm import scoped_session, Session


def admin_registration_form(
    db_session: scoped_session[Session],
) -> List[Dict[str, Any]]:
    role: CustomTypes.RoleEnum = CustomTypes.RoleEnum.ADMIN
    count = 1
    data = []
    for _ in range(count):
        user = UserFactory(role=role.value)
        admin = AdminFactory()

        valid_data = {**user, **admin}
        if "image_path" in valid_data and valid_data["image_path"]:
            local_path = valid_data.pop("image_path")
            valid_data["image_path"] = open(local_path, "rb")
            os.remove(local_path)  # remove the file

        data.append(valid_data)

    return data


def teacher_registration_form(
    db_session: scoped_session[Session],
) -> List[Dict[str, Any]]:
    """Generate a registration form for teachers."""
    role: CustomTypes.RoleEnum = CustomTypes.RoleEnum.TEACHER
    count = 1
    data = []
    for _ in range(count):
        user = UserFactory(role=role.value)
        teacher = TeacherFactory()

        valid_data = {**user, **teacher}
        if "image_path" in valid_data and valid_data["image_path"]:
            local_path = valid_data.pop("image_path")
            valid_data["image_path"] = open(local_path, "rb")
            os.remove(local_path)  # remove the file

        data.append(valid_data)

    return data


def stud_registration_form(db_session: scoped_session[Session]) -> List[Dict[str, Any]]:
    role: CustomTypes.RoleEnum = CustomTypes.RoleEnum.STUDENT
    count: int = 1
    data = []
    for _ in range(count):
        user = UserFactory(role=role.value)
        student = StudentFactory()

        valid_data = {**user, **student}
        if "image_path" in valid_data and valid_data["image_path"]:
            local_path = valid_data.pop("image_path")
            valid_data["image_path"] = open(local_path, "rb")
            os.remove(local_path)  # remove the file

        data.append(valid_data)

    return data


@pytest.fixture(
    params=[
        (CustomTypes.RoleEnum.ADMIN, 1),
        (CustomTypes.RoleEnum.TEACHER, 1),
        (CustomTypes.RoleEnum.STUDENT, 2),
    ],
    ids=["admin_1", "teacher_1", "student_2"],
    scope="module",
)
def registration_form(request, db_session: scoped_session[Session]) -> List[Dict[str, Any]]:
    """Fixture to generate registration forms for different roles."""
    try:
        role: CustomTypes.RoleEnum = request.param[0]
        count: int = request.param[1]
    except (IndexError, TypeError):
        pytest.skip("No role provided for registration form")

    data = []
    factory_map = {
        CustomTypes.RoleEnum.ADMIN: AdminFactory,
        CustomTypes.RoleEnum.TEACHER: TeacherFactory,
        CustomTypes.RoleEnum.STUDENT: StudentFactory,
    }

    for _ in range(count):
        user = UserFactory(role=role.value)
        role_data = factory_map[role]()

        if not user or not role_data:
            pytest.skip(f"No data found for role: {role}")

        valid_data = {**user, **role_data}

        if "image_path" in valid_data and valid_data["image_path"]:
            local_path = valid_data.pop("image_path")
            valid_data["image_path"] = open(local_path, "rb")
            os.remove(local_path)  # remove the file

        data.append(valid_data)

    return data


@pytest.fixture(scope="module")
def register_user(client: FlaskClient, db_session: scoped_session[Session]) -> None:
    registration_form = (
        admin_registration_form(db_session)
        + teacher_registration_form(db_session)
        + stud_registration_form(db_session)
    )
    for valid_data in registration_form:
        # Send a POST request to the registration endpoint
        response = client.post(
            f"/api/v1/registration/{valid_data['role']}", data=valid_data
        )

        # Assert that the registration was successful
        assert response.status_code == 201
        assert (
            response.json["message"] == f"{valid_data['role']} registered successfully!"
        )


@pytest.fixture(scope="function")
def register_user_temp(
    client: FlaskClient,
    registration_form,
):
    for valid_data in registration_form:
        # Send a POST request to the registration endpoint
        response = client.post(
            f"/api/v1/registration/{valid_data['role']}", data=valid_data
        )

        # Assert that the registration was successful
        assert response.status_code == 201
        assert (
            response.json["message"] == f"{valid_data['role']} registered successfully!"
        )

    yield None
