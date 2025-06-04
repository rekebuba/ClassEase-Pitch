from typing import Any, Dict
from flask.testing import FlaskClient
import pytest

from tests.test_api.factories import EventFactory
from tests.typing import Credential


@pytest.fixture(scope="session")
def create_semester(
    client: FlaskClient, admin_auth_header: Credential
) -> None:  # auth_header -> Admin
    print("Creating semester fixture...")
    event_form = EventFactory.build(purpose="New Semester")
    response = client.post(
        "/api/v1/admin/event/new",
        json=event_form,
        headers=admin_auth_header["header"],
    )

    assert response.status_code == 201
    assert response.json is not None
    assert "message" in response.json
    assert response.json["message"] == "Event Created Successfully"


@pytest.fixture(scope="session")
def create_mark_list(
    client: FlaskClient,
    stud_course_register: None,
    fake_mark_list: Dict[str, Any],
    admin_auth_header: Credential,
) -> None:
    """
    Fixture to create a mark list for testing purposes.
    This fixture assumes that the student has already registered for courses.
    """
    response = client.post(
        "/api/v1/admin/mark-list/new",
        json=fake_mark_list,
        headers=admin_auth_header["header"],
    )

    assert response.status_code == 201
    assert response.json is not None
    assert "message" in response.json
    assert response.json["message"] == "Mark list created successfully!"
