#!/usr/bin/python

from sqlalchemy.orm import scoped_session, Session
from flask import Flask
from flask.testing import FlaskClient
import pytest
from models import storage
from typing import Iterator
from tests import remove_json_file, test_app


@pytest.fixture(scope="session", autouse=True)
def app_session() -> Iterator[Flask]:
    """Session-scoped fixture for the Flask app."""

    yield test_app

    storage.rollback()
    storage.session.remove()
    storage.drop_all()

    remove_json_file("student_sort_query.json")
    remove_json_file("student_sort_advance_query.json")


@pytest.fixture(scope="session")
def db_session() -> Iterator[scoped_session[Session]]:
    """Function-scoped fixture for database transactions."""
    yield storage.session

    storage.rollback()  # Roll back the transaction after the test


@pytest.fixture(scope="session")
def client(app_session: Flask) -> Iterator[FlaskClient]:
    """Session-scoped fixture for the Flask test client."""
    with app_session.test_client() as client:
        yield client
