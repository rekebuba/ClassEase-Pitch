from flask.testing import FlaskClient
import pytest

from tests.typing import Credential


@pytest.fixture(scope="module")
def create_semester(client: FlaskClient, admin_auth_header: Credential, event_form):  # auth_header -> Admin
    response = client.post(
        "/api/v1/admin/event/new",
        json=event_form,
        headers=admin_auth_header["header"],
    )

    assert response.status_code == 201
    assert response.json["message"] == "Event Created Successfully"


@pytest.fixture(scope="module")
def create_mark_list(client: FlaskClient, stud_course_register, fake_mark_list, admin_auth_header):
    response = client.post(
        "/api/v1/admin/mark-list/new",
        json=fake_mark_list,
        headers=admin_auth_header["header"],
    )

    assert response.status_code == 201
    assert response.json["message"] == "Mark list created successfully!"
