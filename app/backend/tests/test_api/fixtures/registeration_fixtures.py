#!/usr/bin/python

from typing import Iterator
from flask.testing import FlaskClient
import pytest
from models.admin import Admin
from models.student import Student
from models.teacher import Teacher
from tests.factories.models import (
    AdminFactory,
    StudentFactory,
    TeacherFactory,
)
from sqlalchemy.orm import scoped_session, Session


@pytest.fixture(scope="session")
def create_admin(
    client: FlaskClient, db_session: scoped_session[Session]
) -> Iterator[Admin]:
    yield AdminFactory.create()


@pytest.fixture(scope="session")
def create_teacher(
    client: FlaskClient, db_session: scoped_session[Session]
) -> Iterator[Teacher]:
    yield TeacherFactory.create()


@pytest.fixture(scope="session")
def create_student(
    client: FlaskClient, db_session: scoped_session[Session]
) -> Iterator[Student]:
    yield StudentFactory.create()
