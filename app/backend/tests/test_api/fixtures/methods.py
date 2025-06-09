from typing import Any, Dict, Optional

import pytest
from models.base_model import CustomTypes
from models.user import User
from tests.test_api.factories import AdminFactory, StudentFactory, TeacherFactory
from sqlalchemy.orm import scoped_session, Session


all_params: Dict[str, Any] = {
    "test_users_log_in_success": {
        "params": "role",
        "values": [
            (CustomTypes.RoleEnum.ADMIN, 1),
            (CustomTypes.RoleEnum.TEACHER, 1),
            (CustomTypes.RoleEnum.STUDENT, 1),
        ],
        "ids": ["Admin", "Teacher", "Student"],
    },
    "test_users_dashboard_information": {
        "params": "role",
        "values": [
            (CustomTypes.RoleEnum.ADMIN, 1),
            (CustomTypes.RoleEnum.TEACHER, 1),
            (CustomTypes.RoleEnum.STUDENT, 1),
        ],
        "ids": ["Admin", "Teacher", "Student"],
    },
    "test_each_user_registration": {
        "params": "register_user_temp",
        "values": [
            (AdminFactory, 1),
            (TeacherFactory, 1),
            (StudentFactory, 2),
        ],
        "ids": ["Admin", "Teacher", "Student"],
    },
}


def pytest_generate_tests(metafunc):
    fct_name = metafunc.function.__name__
    if fct_name in all_params:
        params = all_params[fct_name]
        print("FUNCTION NAME:", fct_name)
        print("PARAMS:", params)
        metafunc.parametrize(
            params["params"],
            params["values"],
            ids=params["ids"],
            indirect=True,
        )


@pytest.fixture
def role(
    request: pytest.FixtureRequest, db_session: scoped_session[Session]
) -> list[User]:
    """
    Fixture to get a user based on role and count.
    """
    role, count = request.param
    user = db_session.query(User).filter(User.role == role).limit(count).all()

    return user


@pytest.fixture
def random_admin(db_session: scoped_session[Session]) -> User:
    """
    Fixture to get a user based on role and count.
    """
    admin = (
        db_session.query(User).filter(User.role == CustomTypes.RoleEnum.ADMIN).first()
    )

    # Ensure the admin is not None
    if not admin:
        pytest.skip("No admin user found in the database for authentication.")

    return admin


@pytest.fixture
def random_student(db_session: scoped_session[Session]) -> User:
    """
    Fixture to get a user based on role and count.
    """
    student = (
        db_session.query(User).filter(User.role == CustomTypes.RoleEnum.STUDENT).first()
    )

    # Ensure the student is not None
    if not student:
        pytest.skip("No student user found in the database for authentication.")

    return student


@pytest.fixture
def random_teacher(db_session: scoped_session[Session]) -> User:
    """
    Fixture to get a user based on role and count.
    """
    teacher = (
        db_session.query(User).filter(User.role == CustomTypes.RoleEnum.TEACHER).first()
    )

    # Ensure the teacher is not None
    if not teacher:
        pytest.skip("No teacher user found in the database for authentication.")

    return teacher


def prepare_form_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively flatten nested dictionary into form-compatible format
    and separate files for multipart form upload.
    """
    form_data = {}

    for key, value in data.items():
        if isinstance(value, dict):
            # Handle nested dictionaries by flattening keys (e.g., {"user": {"name": "John"}} becomes "user.name")
            for sub_key, sub_value in value.items():
                nested_key = f"{key}.{sub_key}"
                form_data[nested_key] = sub_value
        else:
            form_data[key] = value

    return form_data
