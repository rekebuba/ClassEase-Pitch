#!/usr/bin/python

import pytest
import unittest
from api import create_app
from models.engine.db_storage import DBStorage
from models.user import User
from models.base_model import Base, BaseModel
from models.grade import Grade, seed_grades
from contextlib import contextmanager
from tests.test_api.factories import *
import os
import json
import random
from models.admin import Admin
from tests.test_api.helper_functions import *
from models import storage
from datetime import date


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


@contextmanager
def override_session(session, *factories):
    """Temporarily override the sqlalchemy_session for multiple factories."""
    original_sessions = {
        factory: factory._meta.sqlalchemy_session for factory in factories}

    try:
        for factory in factories:
            factory._meta.sqlalchemy_session = session
        yield
    finally:
        for factory, original_session in original_sessions.items():
            factory._meta.sqlalchemy_session = original_session


@pytest.fixture(params=[(AdminFactory, 'admin'), (TeacherFactory, 'teacher'), (StudentFactory, 'student'),])
# @pytest.fixture(params=[(TeacherFactory, 'teacher'),])
def user_register_success(request, client, db_session):
    factory, role = request.param
    with override_session(db_session, factory, UserFactory):
        user = factory(role=role)

        # Convert the user object to a dictionary
        user_data = user.to_dict()
        valid_data = {
            **(user_data.pop('user')).to_dict(),
            **user_data
        }

        valid_data.pop('id')
        valid_data.pop('created_at')
        valid_data.pop('updated_at')
        valid_data.pop('__class__')
        valid_data.pop('role')
        valid_data.pop('identification')
        valid_data.pop('password') if 'password' in valid_data else None
        valid_data.pop(
            'sqlalchemy_session') if 'sqlalchemy_session' in valid_data else None
        user_data.pop('semester_id') if 'semester_id' in valid_data else None
        print(valid_data)

        if 'image_path' in valid_data:
            local_path = valid_data.pop('image_path')
            valid_data['image_path'] = open(local_path, 'rb')
            os.remove(local_path)  # remove the file

    return valid_data, role


@pytest.fixture(params=[(AdminFactory, 'admin'), (TeacherFactory, 'teacher'), (StudentFactory, 'student'),])
def role_based_user(request, db_session):
    factory, role = request.param

    with override_session(db_session, factory, UserFactory):
        user = factory(role=role)

        db_session.commit()

    return user


def user_auth_header(client, role_based_user):
    # Log in the user once and reuse the token
    response = client.post('/api/v1/auth/login', json={
        'id': role_based_user.user.identification,
        'password': role_based_user.user.identification
    })

    token = response.json["apiKey"]

    return {"Authorization": f"Bearer {token}"}
