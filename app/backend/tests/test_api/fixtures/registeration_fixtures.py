#!/usr/bin/python

from typing import Any
from flask.testing import FlaskClient
import pytest
from tests.test_api.factories import (
    AdminFactory,
    StudentFactory,
    TeacherFactory,
)
from sqlalchemy.orm import scoped_session, Session
from tests.test_api.fixtures.methods import prepare_form_data


@pytest.fixture(scope="session")
def register_admin(client: FlaskClient, db_session: scoped_session[Session]) -> None:
    admin = AdminFactory.build()
    form_data = prepare_form_data(admin)

    # Send a POST request to the registration endpoint
    response = client.post(
        f"/api/v1/registration/{admin['user']['role']}", data=form_data
    )

    # Assert that the registration was successful
    assert response.status_code == 201
    assert response.json is not None
    assert "message" in response.json
    assert (
        response.json["message"] == f"{admin['user']['role']} registered successfully!"
    )


@pytest.fixture(scope="session")
def register_teacher(client: FlaskClient, db_session: scoped_session[Session]) -> None:
    teacher = TeacherFactory.build()
    form_data = prepare_form_data(teacher)

    # Send a POST request to the registration endpoint
    response = client.post(
        f"/api/v1/registration/{teacher['user']['role']}", data=form_data
    )

    # Assert that the registration was successful
    assert response.status_code == 201
    assert response.json is not None
    assert "message" in response.json
    assert (
        response.json["message"]
        == f"{teacher['user']['role']} registered successfully!"
    )


@pytest.fixture(scope="session")
def register_student(client: FlaskClient, db_session: scoped_session[Session]) -> None:
    student = StudentFactory.build()
    form_data = prepare_form_data(student)

    # Send a POST request to the registration endpoint
    response = client.post(
        f"/api/v1/registration/{student['user']['role']}", data=form_data
    )

    # Assert that the registration was successful
    assert response.status_code == 201
    assert response.json is not None
    assert "message" in response.json
    assert (
        response.json["message"]
        == f"{student['user']['role']} registered successfully!"
    )


@pytest.fixture(scope="function")
def register_user_temp(
    client: FlaskClient,
    request: pytest.FixtureRequest,
) -> Any:
    Factory, count = request.param
    valid_data = Factory.build()
    form_data = prepare_form_data(valid_data)

    # Send a POST request to the registration endpoint
    response = client.post(
        f"/api/v1/registration/{valid_data['user']['role']}",
        data=form_data,
    )

    # Assert that the registration was successful
    assert response.status_code == 201
    assert response.json is not None
    assert "message" in response.json
    assert (
        response.json["message"]
        == f"{valid_data['user']['role']} registered successfully!"
    )

    yield None
