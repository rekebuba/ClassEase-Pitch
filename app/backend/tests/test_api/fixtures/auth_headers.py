from typing import Dict
from flask.testing import FlaskClient
import pytest
from extension.enums.enum import RoleEnum
from models.user import User
from tests.factories.models.user_factory import UserFactory
from tests.test_api.fixtures.methods import get_auth_header
from tests.typing import Credential
from sqlalchemy.orm import scoped_session, Session


@pytest.fixture(scope="session")
def admin_auth_header(
    db_session: scoped_session[Session],
    client: FlaskClient,
    create_admin: User,
) -> Credential:
    """Fixture to authenticate as an admin user and return the auth header."""
    return get_auth_header(
        client, create_admin.identification, create_admin.identification
    )


@pytest.fixture(scope="session")
def stud_auth_header(
    db_session: scoped_session[Session],
    client: FlaskClient,
    create_student: User,
) -> Credential:
    return get_auth_header(
        client,
        create_student.identification,
        create_student.identification,
    )


@pytest.fixture(scope="session")
def teacher_auth_header(
    db_session: scoped_session[Session],
    client: FlaskClient,
    create_teacher: User,
) -> Credential:
    """Fixture to authenticate as a teacher user and return the auth header."""
    return get_auth_header(
        client,
        create_teacher.identification,
        create_teacher.identification,
    )


@pytest.fixture(
    scope="session",
    params=[
        RoleEnum.ADMIN,
        RoleEnum.TEACHER,
        RoleEnum.STUDENT,
    ],
    ids=["Admin", "Teacher", "Student"],
)
def random_auth_header(
    db_session: scoped_session[Session],
    client: FlaskClient,
    request: pytest.FixtureRequest,
) -> Credential:
    """Fixture to authenticate as a random user and return the auth header."""
    role: RoleEnum = request.param

    none_values_map: Dict[RoleEnum, dict[str, None]] = {
        RoleEnum.STUDENT: {"teacher": None, "admin": None},
        RoleEnum.TEACHER: {"student": None, "admin": None},
        RoleEnum.ADMIN: {"student": None, "teacher": None},
    }

    random_user = UserFactory.create(role=role, **none_values_map[role])

    return get_auth_header(
        client,
        random_user.identification,
        random_user.identification,
    )
