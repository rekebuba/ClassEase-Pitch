#!/usr/bin/python

import pytest
from tests.test_api.factories_methods import MakeFactory
from tests.test_api.factories import (
    AdminFactory,
    DefaultFelids,
    StudentFactory,
    TeacherFactory,
    UserFactory,
)
import os
import random
from models.base_model import CustomTypes


@pytest.fixture(
    params=[(CustomTypes.RoleEnum.ADMIN, 1)], ids=["admin<1>"], scope="module"
)
def admin_registration_form(request, db_session):
    role, count = request.param
    data = []
    for _ in range(count):
        user = MakeFactory(UserFactory, db_session, built=True).factory(role=role)
        admin = MakeFactory(AdminFactory, db_session, built=True).factory()

        valid_data = {**user, **admin}
        if "image_path" in valid_data and valid_data["image_path"]:
            local_path = valid_data.pop("image_path")
            valid_data["image_path"] = open(local_path, "rb")
            os.remove(local_path)  # remove the file

        data.append(valid_data)

    return data


@pytest.fixture(
    params=[(CustomTypes.RoleEnum.TEACHER, 1)], ids=["teacher<1>"], scope="module"
)
def teacher_registration_form(request, db_session):
    role, count = request.param
    data = []
    for _ in range(count):
        user = MakeFactory(UserFactory, db_session, built=True).factory(role=role)
        teacher = MakeFactory(TeacherFactory, db_session, built=True).factory()

        valid_data = {**user, **teacher}
        if "image_path" in valid_data and valid_data["image_path"]:
            local_path = valid_data.pop("image_path")
            valid_data["image_path"] = open(local_path, "rb")
            os.remove(local_path)  # remove the file

        data.append(valid_data)

    return data


@pytest.fixture(
    params=[(CustomTypes.RoleEnum.STUDENT, 1)], ids=["student<1>"], scope="module"
)
def stud_registration_form(request, db_session):
    role, count = request.param
    data = []
    for _ in range(count):
        user = MakeFactory(UserFactory, db_session, built=True).factory(role=role)

        current_grade = random.randint(1, 10)
        academic_year = DefaultFelids.current_EC_year()

        student = MakeFactory(StudentFactory, db_session, built=True).factory(
            add={"current_grade": current_grade, "academic_year": academic_year}
        )

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
    ids=["admin<1>", "teacher<1>", "student<2>"],
    scope="module",
)
def registration_form(request, db_session):
    role, count = request.param if request.param else (None, 0)

    data = []
    role_user = {}
    for _ in range(count):
        user = MakeFactory(UserFactory, db_session, built=True).factory(role=role)
        if role == CustomTypes.RoleEnum.STUDENT:
            current_grade = random.randint(1, 10)
            academic_year = DefaultFelids.current_EC_year()
            role_user = MakeFactory(StudentFactory, db_session, built=True).factory(
                add={"current_grade": current_grade, "academic_year": academic_year}
            )
        elif role == CustomTypes.RoleEnum.TEACHER:
            role_user = MakeFactory(TeacherFactory, db_session, built=True).factory()
        elif role == CustomTypes.RoleEnum.ADMIN:
            role_user = MakeFactory(AdminFactory, db_session, built=True).factory()

        valid_data = {**user, **role_user}

        if "image_path" in valid_data and valid_data["image_path"]:
            local_path = valid_data.pop("image_path")
            valid_data["image_path"] = open(local_path, "rb")
            os.remove(local_path)  # remove the file

        data.append(valid_data)

    return data


@pytest.fixture(scope="module")
def register_user(
    client,
    admin_registration_form,
    teacher_registration_form,
    stud_registration_form,
):
    registration_form = (
        admin_registration_form + teacher_registration_form + stud_registration_form
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
    client,
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
            response.json["message"]
            == f"{valid_data['role']} registered successfully!"
        )

    yield None
