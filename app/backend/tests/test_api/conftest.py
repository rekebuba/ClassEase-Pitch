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
    factories = [(AdminFactory, 1), (TeacherFactory, 1), (StudentFactory, 1)]

    users = []
    user = None
    for Factory, count in factories:
        with override_session(db_session, Factory, UserFactory):
            for _ in range(count):
                if Factory == StudentFactory:
                    user = Factory(
                        start_year_id=db_session.query(Year.id).scalar(),
                        current_year_id=db_session.query(Year.id).scalar(),
                    )
                else:
                    user = Factory()

                users.append(user)

        db_session.commit()

    return users


@pytest.fixture(scope="session")
def role(request):
    return request.param


@pytest.fixture(scope="session")
def users_auth_header(client, db_session, role):
    user = db_session.query(User.identification).filter_by(role=role).first()
    response = client.post('/api/v1/auth/login', json={
        'id': user.identification,
        'password': user.identification
    })

    token = response.json["apiKey"]
    return {"Authorization": f"Bearer {token}"}


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
def course_registration(db_session):
    student_data = db_session.query(Student).first()
    subjects = (
        storage.session.query(
            Subject.name.label("subject"),
            Subject.code.label("subject_code"),
            Grade.name.label("grade")
        )
        .join(Grade, Grade.id == Subject.grade_id)
        .filter(Grade.name == (student_data.next_grade if student_data.next_grade else student_data.current_grade))
        .all()
    )

    subject_list = [{key: value for key, value in q._asdict().items()}
                    for q in subjects]

    return {"course": subject_list, "semester": 1, "academic_year": 2017, "grade": subject_list[0]['grade']}


@pytest.fixture(scope="session")
def db_course_registration(db_session, course_registration):
    user_id = db_session.query(User.id).filter_by(role='student').scalar()
    grade_id = db_session.query(Grade.id).filter_by(
        name=course_registration['grade']).scalar()
    semester_id = db_session.query(Semester.id).filter_by(
        name=course_registration['semester']).scalar()

    new_semester_record = STUDSemesterRecord(
        user_id=user_id,
        semester_id=semester_id,
        grade_id=grade_id,
    )
    storage.add(new_semester_record)
    storage.session.flush()

    new_assessment = []
    for course in course_registration['course']:
        subject_id = db_session.query(Subject.id).filter_by(
            name=course['subject'], code=course['subject_code']).scalar()

        new_assessment.append(
            Assessment(
                user_id=user_id,
                subject_id=subject_id,
                semester_record_id=new_semester_record.id,
            )
        )

    storage.session.bulk_save_objects(new_assessment)

    storage.session.execute(
        update(Student)
        .where(Student.user_id == user_id)
        .values(
            semester_id=semester_id,
            current_grade=grade_id,
            next_grade=None,
            has_passed=False,
            is_registered=True,
            is_active=True,
            updated_at=datetime.utcnow()
        )
    )

    storage.save()


@pytest.fixture(scope="session")
def fake_mark_list(db_session):
    subjects = db_session.query(Subject).all()
    custom_subjects = [
        AvailableSubject("Math", "MTH101"),
        AvailableSubject("Science", "SCI102")
    ]

    mark_list = MarkListFactory.create_batch(2, subjects=custom_subjects)
    for mark in mark_list:
        print(json.dumps(mark.to_dict(), indent=4, sort_keys=True))

    return [
        {
            "grade": 1,
            "subjects": [
                {"subject": "English", "subject_code": "ENG2"},
                {"subject": "Maths", "subject_code": "MTH2"}
            ],
            "assessment_type": [
                {"type": "Test 1", "percentage": 25},
                {"type": "Test 2", "percentage": 25},
                {"type": "Test 3", "percentage": 25},
                {"type": "Test 4", "percentage": 25}
            ]
        },
    ]
