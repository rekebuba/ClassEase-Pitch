#!/usr/bin/python

import pytest
import unittest
from api import create_app
from models.subject import Subject
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
from sqlalchemy import update, and_
from tests.test_api.helper_functions import *
from models import storage


@pytest.fixture(scope="session")
def app_session():
    """Session-scoped fixture for the Flask app."""
    app = create_app("testing")

    storage = DBStorage()
    storage.init_app(app)

    yield app

    storage.session.close_all()  # Clean up the database after the session
    storage.drop_all()


@pytest.fixture(scope="session")
def db_session(app_session):
    """Function-scoped fixture for database transactions."""
    storage = DBStorage()
    storage.init_app(app_session)
    yield storage.session

    storage.rollback()  # Roll back the transaction after the test


@pytest.fixture(scope="session")
def client(app_session):
    """Session-scoped fixture for the Flask test client."""
    with app_session.test_client() as client:
        yield client


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
    Factory, count = request.param

    data = []
    with override_session(db_session, Factory, UserFactory):
        for _ in range(count):
            user_data = Factory.build().to_dict()
            valid_data = {
                **(user_data.pop('user')).to_dict(),
                **user_data
            }

            # Remove unnecessary fields
            role = valid_data.pop('role')

            if 'image_path' in valid_data:
                local_path = valid_data.pop('image_path')
                valid_data['image_path'] = open(local_path, 'rb')
                os.remove(local_path)  # remove the file

            data.append((valid_data, role))

    return data


@pytest.fixture(scope="session")
def db_create_users(db_session):
    factories = [(AdminFactory, 1), (TeacherFactory, 1), (StudentFactory, 5)]

    users = []
    user = None
    for Factory, count in factories:
        with override_session(db_session, Factory, UserFactory):
            for _ in range(count):
                if Factory == StudentFactory:
                    current_grade = random.randint(1, 10)

                    user = Factory(
                        start_year_id=db_session.query(Year.id).scalar(),
                        current_year_id=db_session.query(Year.id).scalar(),
                        current_grade_id=db_session.query(Grade.id).filter_by(
                            name=current_grade).scalar(),
                    )
                else:
                    user = Factory()

                users.append(user)

        db_session.commit()

    return users


def user_list(db_session):
    users = db_session.query(User).all()
    return users


@pytest.fixture(scope="session")
def role(request, db_session):
    role, count = request.param
    user = db_session.query(User).filter_by(
        role=role).limit(100 if count == 'all' else count).all()

    return user


@pytest.fixture(scope="session")
def users_auth_header(client, db_session, role):
    auth_headers = []
    for user in role:
        response = client.post('/api/v1/auth/login', json={
            'id': user.identification,
            'password': user.identification
        })
        token = response.json["apiKey"]
        auth_headers.append(
            {"header": {"Authorization": f"Bearer {token}"}, "user": user})

    return auth_headers


@pytest.fixture
def event_form(db_session):
    with override_session(db_session, SemesterFactory, EventFactory):
        form = SemesterFactory.build().to_dict()

        semester_form = {
            **(form.pop('event')).to_dict(),
            'semester': {
                **form
            }
        }

    return semester_form


@pytest.fixture(scope="session")
def db_event_form(db_session):
    with override_session(db_session, SemesterFactory, EventFactory):
        form = SemesterFactory(
            event__year_id=db_session.query(Year.id).scalar(),
        ).to_dict()

        db_session.commit()

    return form


@pytest.fixture(scope="session")
def db_course_registration(db_session):
    students = (db_session.query(Student)
                .join(User, User.id == Student.user_id)
                .filter(User.role == 'student')
                .all()
                )

    for student in students:
        current_grade = (db_session.query(Grade.name)
                         .filter(Grade.id == student.current_grade_id)
                         .scalar()
                         )
        grade_id = (db_session.query(Grade.id)
                    .filter(Grade.name == (current_grade + 1))
                    .scalar()
                    )
        semester_id = (db_session.query(
            Semester.id).filter_by(name=1).scalar())

        new_semester_record = STUDSemesterRecord(
            user_id=student.id,
            semester_id=semester_id,
            grade_id=grade_id,
        )
        storage.add(new_semester_record)
        storage.session.flush()

        subjects = (
            db_session.query(
                Subject.name.label("subject"),
                Subject.code.label("subject_code"),
                Grade.name.label("grade")
            )
            .join(Grade, Grade.id == Subject.grade_id)
            .filter(Grade.id == (student.next_grade_id if student.next_grade_id else student.current_grade_id))
            .all()
        )

        for subject in subjects:
            new_assessment = []
            subject_id = db_session.query(Subject.id).filter_by(
                name=subject.subject, code=subject.subject_code).scalar()

            new_assessment.append(
                Assessment(
                    user_id=student.id,
                    subject_id=subject_id,
                    semester_record_id=new_semester_record.id,
                )
            )

            storage.session.bulk_save_objects(new_assessment)

            storage.session.execute(
                update(Student)
                .where(Student.user_id == student.id)
                .values(
                    semester_id=semester_id,
                    current_grade_id=grade_id,
                    next_grade_id=None,
                    has_passed=False,
                    is_registered=True,
                    is_active=True,
                    updated_at=datetime.utcnow()
                )
            )

            storage.save()


@pytest.fixture(scope="session")
def fake_mark_list(db_session):
    # generate fake mark list for each grade
    mark_list = MarkListFactory().to_dict()
    for assessment in mark_list['mark_assessment']:
        subjects = (db_session.query(Subject.name, Subject.code)
                    .join(Grade, Grade.id == Subject.grade_id)
                    .filter(Grade.name == assessment['grade'])
                    .all()
                    )
        custom_subjects = [AvailableSubject(
            subject=name, subject_code=code, grade=assessment['grade']).to_dict() for name, code in subjects]
        assessment['subjects'] = custom_subjects

    # print(json.dumps(mark_list, indent=4, sort_keys=True))

    return mark_list
