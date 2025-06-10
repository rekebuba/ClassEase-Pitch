from flask.testing import FlaskClient
import pytest
from models.admin import Admin
from models.student import Student
from models.teacher import Teacher
from tests.typing import Credential
from sqlalchemy.orm import scoped_session, Session


@pytest.fixture(scope="session")
def admin_auth_header(
    db_session: scoped_session[Session],
    client: FlaskClient,
    create_admin: Admin,
) -> Credential:
    """Fixture to authenticate as an admin user and return the auth header."""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "id": create_admin.user.identification,
            "password": create_admin.user.identification,
        },
    )

    assert response.status_code == 200
    assert response.json is not None
    assert "apiKey" in response.json

    token = response.json["apiKey"]
    return {"header": {"apiKey": f"Bearer {token}"}}


@pytest.fixture(scope="session")
def stud_auth_header(
    db_session: scoped_session[Session],
    client: FlaskClient,
    create_student: Student,
) -> Credential:
    response = client.post(
        "/api/v1/auth/login",
        json={
            "id": create_student.user.identification,
            "password": create_student.user.identification,
        },
    )

    assert response.status_code == 200
    assert response.json is not None
    assert "apiKey" in response.json

    token = response.json["apiKey"]
    return {"header": {"apiKey": f"Bearer {token}"}}


@pytest.fixture(scope="session")
def teacher_auth_header(
    db_session: scoped_session[Session],
    client: FlaskClient,
    create_teacher: Teacher,
) -> Credential:
    """Fixture to authenticate as a teacher user and return the auth header."""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "id": create_teacher.user.identification,
            "password": create_teacher.user.identification,
        },
    )

    assert response.status_code == 200
    assert response.json is not None
    assert "apiKey" in response.json

    token = response.json["apiKey"]
    return {"header": {"apiKey": f"Bearer {token}"}}
