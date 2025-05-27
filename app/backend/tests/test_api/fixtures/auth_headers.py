from typing import Any, Dict, Iterator, TypedDict
from flask.testing import FlaskClient
import pytest
from tests.typing import Credential
from models.user import User
from models.base_model import CustomTypes
from sqlalchemy.orm import scoped_session, Session


@pytest.fixture
def users_auth_header(client: FlaskClient, register_user, role):
    auth_headers = []
    for user in role:
        response = client.post(
            "/api/v1/auth/login",
            json={"id": user.identification, "password": user.identification},
        )
        token = response.json["apiKey"]
        auth_headers.append({"header": {"apiKey": f"Bearer {token}"}, "user": user})

    return auth_headers


@pytest.fixture(scope="module")
def all_admin_auth_header(
    db_session: scoped_session[Session], client: FlaskClient, register_user
):
    auth_headers = []
    role = CustomTypes.RoleEnum.ADMIN
    admins = db_session.query(User).filter(User.role == role).all()

    for user in admins:
        response = client.post(
            "/api/v1/auth/login",
            json={"id": user.identification, "password": user.identification},
        )
        token = response.json["apiKey"]
        auth_headers.append({"header": {"apiKey": f"Bearer {token}"}, "user": user})

    return auth_headers


@pytest.fixture(scope="module")
def all_teacher_auth_header(
    db_session: scoped_session[Session], client: FlaskClient, register_user
):
    auth_headers = []
    role = CustomTypes.RoleEnum.TEACHER
    teachers = db_session.query(User).filter(User.role == role).all()

    for user in teachers:
        response = client.post(
            "/api/v1/auth/login",
            json={"id": user.identification, "password": user.identification},
        )
        token = response.json["apiKey"]
        auth_headers.append({"header": {"apiKey": f"Bearer {token}"}, "user": user})

    return auth_headers


@pytest.fixture(scope="module")
def all_stud_auth_header(
    db_session: scoped_session[Session], client: FlaskClient, register_user
):
    auth_headers = []
    role = CustomTypes.RoleEnum.STUDENT
    students = db_session.query(User).filter(User.role == role).all()

    for user in students:
        response = client.post(
            "/api/v1/auth/login",
            json={"id": user.identification, "password": user.identification},
        )
        token = response.json["apiKey"]
        auth_headers.append({"header": {"apiKey": f"Bearer {token}"}, "user": user})

    return auth_headers


@pytest.fixture(scope="module")
def admin_auth_header(
    db_session: scoped_session[Session], client: FlaskClient, register_user: None
) -> Credential:
    role = CustomTypes.RoleEnum.ADMIN

    user = db_session.query(User).filter(User.role == role).first()
    if not user:
        pytest.skip("No admin user found in the database for authentication.")
    response = client.post(
        "/api/v1/auth/login",
        json={"id": user.identification, "password": user.identification},
    )

    assert response.status_code == 200
    assert response.json is not None
    assert "apiKey" in response.json

    token = response.json["apiKey"]
    return {"header": {"apiKey": f"Bearer {token}"}}


@pytest.fixture(scope="module")
def stud_auth_header(
    db_session: scoped_session[Session], client: FlaskClient, register_user
):
    role = CustomTypes.RoleEnum.STUDENT

    user = db_session.query(User).filter(User.role == role).first()

    response = client.post(
        "/api/v1/auth/login",
        json={"id": user.identification, "password": user.identification},
    )

    assert response.status_code == 200
    assert "apiKey" in response.json

    token = response.json["apiKey"]
    return {"header": {"apiKey": f"Bearer {token}"}, "user": user}


@pytest.fixture(scope="module")
def teacher_auth_header(
    db_session: scoped_session[Session], client: FlaskClient, register_user
):
    role = CustomTypes.RoleEnum.TEACHER

    user = db_session.query(User).filter(User.role == role).first()

    response = client.post(
        "/api/v1/auth/login",
        json={"id": user.identification, "password": user.identification},
    )

    assert response.status_code == 200
    assert "apiKey" in response.json

    token = response.json["apiKey"]
    return {"header": {"apiKey": f"Bearer {token}"}, "user": user}
