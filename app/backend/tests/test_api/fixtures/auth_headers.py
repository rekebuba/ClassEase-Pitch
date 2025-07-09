from flask.testing import FlaskClient
import pytest
from models.student import Student
from models.teacher import Teacher
from models.user import User
from tests.typing import Credential
from sqlalchemy.orm import scoped_session, Session


@pytest.fixture(scope="session")
def admin_auth_header(
    db_session: scoped_session[Session],
    client: FlaskClient,
    create_admin: User,
) -> Credential:
    """Fixture to authenticate as an admin user and return the auth header."""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "identification": create_admin.identification,
            "password": create_admin.identification,
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
            "identification": create_student.user.identification,
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
    create_teacher: User,
) -> Credential:
    """Fixture to authenticate as a teacher user and return the auth header."""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "identification": create_teacher.identification,
            "password": create_teacher.identification,
        },
    )

    assert response.status_code == 200
    assert response.json is not None
    assert "apiKey" in response.json

    token = response.json["apiKey"]
    return {"header": {"apiKey": f"Bearer {token}"}}
