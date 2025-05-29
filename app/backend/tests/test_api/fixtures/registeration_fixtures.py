#!/usr/bin/python

from flask.testing import FlaskClient
import pytest
from tests.test_api.factories import (
    AdminFactory,
    StudentFactory,
    TeacherFactory,
)
from sqlalchemy.orm import scoped_session, Session

from tests.test_api.fixtures.methods import prepare_form_data


@pytest.fixture(scope="module")
def register_user(client: FlaskClient, db_session: scoped_session[Session]) -> None:
    registration_form = [
        AdminFactory(),
        *StudentFactory.create_batch(2),
        TeacherFactory(),
    ]
    for valid_data in registration_form:
        form_data = prepare_form_data(valid_data)

        # Send a POST request to the registration endpoint
        response = client.post(
            f"/api/v1/registration/{valid_data['user']['role']}", data=form_data
        )

        # Assert that the registration was successful
        assert response.status_code == 201
        assert response.json is not None
        assert "message" in response.json
        assert (
            response.json["message"]
            == f"{valid_data['user']['role']} registered successfully!"
        )


@pytest.fixture(scope="function")
def register_user_temp(
    client: FlaskClient,
    request: pytest.FixtureRequest,
) -> None:
    Factory, count = request.param
    valid_data = Factory()
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
