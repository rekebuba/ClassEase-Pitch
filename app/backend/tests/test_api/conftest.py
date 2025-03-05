#!/usr/bin/python

import pytest
import unittest
from app.backend.api import create_app
from models.user import User
from models import init_app, storage
import json
import random
from models.admin import Admin
from tests.test_api.helper_functions import *

@pytest.fixture(scope="session")
def app_session():
    """Session-scoped fixture for the Flask app."""
    app = create_app("testing")
    yield app

@pytest.fixture(scope="session")
def client(app_session):
    """Session-scoped fixture for the Flask test client."""
    with app_session.test_client() as client:
        yield client

@pytest.fixture(scope="session")
def database(app_session):
    """Session-scoped fixture for the database."""
    with app_session.app_context():
        pass

@pytest.fixture(scope="function")
def db_session(database):
    """Function-scoped fixture for database transactions."""
    connection = database.engine.connect()
    transaction = connection.begin()
    session = database.create_scoped_session(options={"bind": connection})

    database.session = session
    yield session

    # Rollback the transaction after the test
    transaction.rollback()
    connection.close()
