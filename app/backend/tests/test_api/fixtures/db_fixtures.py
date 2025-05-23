#!/usr/bin/python

import pytest
from api import create_app
from models import storage


@pytest.fixture(scope="session")
def app_session():
    """Session-scoped fixture for the Flask app."""
    app = create_app("testing")
    # app = create_app("development")

    yield app

    storage.rollback()
    storage.session.remove()
    storage.drop_all()


@pytest.fixture(scope="session")
def db_session(app_session):
    """Function-scoped fixture for database transactions."""
    storage.init_app(app_session)
    yield storage.session

    storage.rollback()  # Roll back the transaction after the test


@pytest.fixture(scope="session")
def client(app_session):
    """Session-scoped fixture for the Flask test client."""
    with app_session.test_client() as client:
        yield client
