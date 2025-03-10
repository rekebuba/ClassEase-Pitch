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
from datetime import date, time


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


@pytest.fixture(scope="session")
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


@pytest.fixture(params=[(AdminFactory, 1), (TeacherFactory, 1), (StudentFactory, 1)])
def user_register_success(request, db_session):
    factory, count = request.param

    data = []
    with override_session(db_session, factory, UserFactory):
        for _ in range(count):
            user = factory()

            # Convert the user object to a dictionary
            user_data = user.to_dict()
            valid_data = {
                **(user_data.pop('user')).to_dict(),
                **user_data
            }

            # Remove unnecessary fields
            role = valid_data.pop('role')
            valid_data.pop('id')
            valid_data.pop('created_at')
            valid_data.pop('updated_at')
            valid_data.pop('__class__')
            valid_data.pop('identification')
            valid_data.pop('sqlalchemy_session')
            valid_data.pop('password') if 'password' in valid_data else None
            user_data.pop(
                'semester_id') if 'semester_id' in valid_data else None

            if 'image_path' in valid_data:
                local_path = valid_data.pop('image_path')
                valid_data['image_path'] = open(local_path, 'rb')
                os.remove(local_path)  # remove the file

            data.append((valid_data, role))

    return data


@pytest.fixture(scope="session")
def db_create_users(db_session):
    factories = [(AdminFactory, 1), (TeacherFactory, 1), (StudentFactory, 1)]

    users = []
    for factory, count in factories:
        with override_session(db_session, factory, UserFactory):
            for _ in range(count):
                user = factory()
                users.append(user)

        db_session.commit()

    return users


@pytest.fixture(scope="session")
def role(request):
    return request.param


@pytest.fixture(scope="session")
def users_auth_header(client, db_session, role):
    id = db_session.query(User.identification).filter_by(role=role).scalar()
    response = client.post('/api/v1/auth/login', json={
        'id': id,
        'password': id
    })

    token = response.json["apiKey"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def event_form(db_session):
    with override_session(db_session, SemesterFactory, EventFactory):
        form = SemesterFactory().to_dict()

        semester_form = {
            **(form.pop('event')).to_dict(),
            'semester': {
                **form
            }
        }

        # Remove unnecessary fields
        semester_form.pop('id')
        semester_form.pop('created_at')
        semester_form.pop('updated_at')
        semester_form.pop('sqlalchemy_session')
        semester_form.pop('__class__')
        semester_form['semester'].pop('event_id')
        semester_form['semester'].pop('id')
        semester_form['semester'].pop('created_at')
        semester_form['semester'].pop('updated_at')
        semester_form['semester'].pop('__class__')

    # Convert date fields to string (ISO format)
    for key, value in semester_form.items():
        if isinstance(value, (date, datetime)):
            if key in ['start_time', 'end_time']:
                semester_form[key] = value.strftime("%H:%M:%S")
            else:
                semester_form[key] = value.strftime("%Y-%m-%d")

    return semester_form


@pytest.fixture(scope="session")
def db_event_form(db_session):
    with override_session(db_session, SemesterFactory, EventFactory):
        form = SemesterFactory().to_dict()

        db_session.commit()

    semester_form = {
        **(form.pop('event')).to_dict(),
        'semester': {
            **form
        }
    }

    return form
