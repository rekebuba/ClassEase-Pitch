#!/usr/bin/python

import pytest
import unittest
from api import create_app
from models.engine.db_storage import DBStorage
from models.user import User
from models.base_model import Base, BaseModel
from models.grade import Grade, seed_grades
import json
import random
from models.admin import Admin
from tests.test_api.helper_functions import *
from models import storage


@pytest.fixture(scope="session")
def app_session():
    """Session-scoped fixture for the Flask app."""
    app = create_app("testing")

    storage = DBStorage()
    storage.init_app(app)

    yield app

    storage.drop_all()  # Clean up the database after the session


@pytest.fixture(scope="session")
def client(app_session):
    """Session-scoped fixture for the Flask test client."""
    with app_session.test_client() as client:
        yield client


@pytest.fixture(scope="function")
def db_session(app_session):
    """Function-scoped fixture for database transactions."""
    storage = DBStorage()
    storage.init_app(app_session)
    yield storage.session

    storage.rollback()  # Roll back the transaction after the test


@pytest.fixture(scope="function")
def admin_registration(client, db_session):
    """Function-scoped fixture for registering an admin."""
    with override_session(AdminFactory, db_session):
        admin = AdminFactory()

        # Convert the admin object to a dictionary
        admin_data = admin.to_dict()

        admin_data.pop('id')
        admin_data.pop('created_at')
        admin_data.pop('updated_at')
        admin_data.pop('__class__')

    # Send a POST request to the registration endpoint
    response = client.post('/api/v1/registration/admin',
                           data=admin_data)

    return response
