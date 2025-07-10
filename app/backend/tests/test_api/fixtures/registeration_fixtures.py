#!/usr/bin/python

from typing import Dict
from flask.testing import FlaskClient
import pytest
from extension.enums.enum import RoleEnum
from models.user import User
from sqlalchemy.orm import scoped_session, Session

from tests.factories.models.user_factory import UserFactory


@pytest.fixture(scope="session")
def create_admin(client: FlaskClient, db_session: scoped_session[Session]) -> User:
    return UserFactory.create(
        role=RoleEnum.ADMIN,
        student=None,
        teacher=None,
    )


@pytest.fixture(scope="session")
def create_teacher(client: FlaskClient, db_session: scoped_session[Session]) -> User:
    return UserFactory.create(
        role=RoleEnum.ADMIN,
        student=None,
        admin=None,
    )


@pytest.fixture(scope="session")
def create_student(client: FlaskClient, db_session: scoped_session[Session]) -> User:
    return UserFactory.create(
        role=RoleEnum.ADMIN,
        teacher=None,
        admin=None,
    )


@pytest.fixture(scope="session")
def create_random_user(
    client: FlaskClient,
    db_session: scoped_session[Session],
    request: pytest.FixtureRequest,
) -> User:
    """Fixture to create a random user."""
    role: RoleEnum = request.param  # ← get the parameter from the testy

    none_values_map: Dict[RoleEnum, dict[str, None]] = {
        RoleEnum.STUDENT: {"teacher": None, "admin": None},
        RoleEnum.TEACHER: {"student": None, "admin": None},
        RoleEnum.ADMIN: {"student": None, "teacher": None},
    }

    return UserFactory.create(role=role, **none_values_map[role])
