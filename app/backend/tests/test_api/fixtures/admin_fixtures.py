import pytest


@pytest.fixture(scope="module")
def create_semester(client, admin_auth_header, event_form):  # auth_header -> Admin
    response = client.post(
        "/api/v1/admin/event/new",
        json=event_form,
        headers=admin_auth_header["header"],
    )

    assert response.status_code == 201
    assert response.json["message"] == "Event Created Successfully"
