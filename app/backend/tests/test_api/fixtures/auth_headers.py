from flask.testing import FlaskClient
import pytest
from models.user import User
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


@pytest.fixture(scope="session")
def random_user_auth_header(
    db_session: scoped_session[Session],
    client: FlaskClient,
    create_random_user: User,
) -> Credential:
    """Fixture to authenticate as a random user and return the auth header."""
    return get_auth_header(
        client,
        create_random_user.identification,
        create_random_user.identification,
    )
