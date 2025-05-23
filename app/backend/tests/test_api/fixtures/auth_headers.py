from typing import List
import pytest
from models.user import User
from models.base_model import CustomTypes
from models import storage


@pytest.fixture
def users_auth_header(client, register_user, role):
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
def all_admin_auth_header(db_session, client, register_user):
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
def all_teacher_auth_header(db_session, client, register_user):
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
def all_stud_auth_header(db_session, client, register_user):
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
def admin_auth_header(db_session, client, register_user):
    role = CustomTypes.RoleEnum.ADMIN

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
def stud_auth_header(db_session, client, register_user):
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
def teacher_auth_header(db_session, client, register_user):
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
