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
from models.base_model import CustomTypes
from .factories_methods import MakeFactory


@pytest.fixture(scope="session")
def app_session():
    """Session-scoped fixture for the Flask app."""
    app = create_app("testing")

    storage = DBStorage()
    storage.init_app(app)

    yield app

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


@pytest.fixture(params=[
    (CustomTypes.RoleEnum.ADMIN, 1),
    (CustomTypes.RoleEnum.TEACHER, 1),
    (CustomTypes.RoleEnum.STUDENT, 5)
])
def register_users(request, db_session):
    role, count = request.param

    data = []
    role_user = None
    for _ in range(count):
        user = MakeFactory(UserFactory, db_session).factory(
            role=role, keep={'id'})
        if role == CustomTypes.RoleEnum.STUDENT:
            current_grade = random.randint(1, 10)
            academic_year = DefaultFelids.current_EC_year()
            role_user = MakeFactory(StudentFactory, db_session).factory(
                user_id=user.pop('id'),
                start_year_id=db_session.query(Year.id).scalar(),
                current_year_id=db_session.query(Year.id).scalar(),
                current_grade_id=db_session.query(Grade.id).filter_by(
                    name=current_grade).scalar(),
                add={"current_grade": current_grade,
                     "academic_year": academic_year}
            )
        elif role == CustomTypes.RoleEnum.TEACHER:
            role_user = MakeFactory(TeacherFactory, db_session).factory(
                user_id=user.pop('id')
            )
        elif role == CustomTypes.RoleEnum.ADMIN:
            role_user = MakeFactory(AdminFactory, db_session).factory(
                user_id=user.pop('id')
            )

        valid_data = {
            **user,
            **role_user
        }

        if 'image_path' in valid_data and valid_data['image_path']:
            local_path = valid_data.pop('image_path')
            valid_data['image_path'] = open(local_path, 'rb')
            os.remove(local_path)  # remove the file

        data.append(valid_data)

    return data


@pytest.fixture(scope="session")
def db_create_users(db_session):
    factories = [
        (MakeFactory(AdminFactory, db_session).factory,
         CustomTypes.RoleEnum.ADMIN, 1),
        (MakeFactory(TeacherFactory, db_session).factory,
         CustomTypes.RoleEnum.TEACHER, 1),
        (MakeFactory(StudentFactory, db_session).factory,
         CustomTypes.RoleEnum.STUDENT, 5)
    ]

    users = []
    user = None
    for Factory, role, count in factories:
        for _ in range(count):
            user = MakeFactory(UserFactory, db_session).factory(
                role=role, keep={'id'})
            if role == CustomTypes.RoleEnum.STUDENT:
                current_grade = random.randint(1, 10)

                role_user = Factory(
                    user_id=user['id'],
                    start_year_id=db_session.query(Year.id).scalar(),
                    current_year_id=db_session.query(Year.id).scalar(),
                    current_grade_id=db_session.query(Grade.id).filter_by(
                        name=current_grade).scalar(),
                )
            else:
                role_user = Factory(user_id=user['id'])

        db_session.commit()
        users.append({"user": user, "role_user": role_user})

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
            {"header": {"apiKey": f"Bearer {token}"}, "user": user})

    return auth_headers


@pytest.fixture
def event_form(db_session):
    event = MakeFactory(EventFactory, db_session).factory(
        add={'academic_year': DefaultFelids.current_EC_year()},
        keep={'id'},
        year_id=db_session.query(Year.id).scalar(),
        purpose='New Semester'
    )
    form = MakeFactory(SemesterFactory, db_session).factory(
        event_id=event.pop('id'))

    semester_form = {
        **event,
        'semester': {
            **form
        },
    }

    return semester_form


@pytest.fixture(scope="session")
def db_course_registration(db_session):
    students = (db_session.query(Student)
                .join(User, User.id == Student.user_id)
                .filter(User.role == 'student')
                .all()
                )

    for student in students:
        grade_id = (db_session.query(Grade.id)
                    .filter(Grade.id == (student.next_grade_id if student.next_grade_id else student.current_grade_id))
                    .scalar()
                    )
        semester_id = (db_session.query(Semester.id)
                       .filter_by(name=(1 if not student.next_grade_id else 2))
                       .scalar()
                       )

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
            .filter(Grade.id == grade_id)
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
    registered_students = (db_session.query(Grade.name)
                           .join(STUDSemesterRecord, STUDSemesterRecord.grade_id == Grade.id)
                           .all()
                           )

    available_teachers = (db_session.query(User.identification)
                          .join(Teacher, User.id == Teacher.user_id)
                          .all()
                          )

    grades = {grade.name for grade in registered_students}
    mark_list = MarkListFactory(count=len(grades)).to_dict()
    mark_list.pop('count')

    for grade, assessment in zip(list(grades), mark_list['mark_assessment']):
        assessment['grade'] = grade
        subjects = (db_session.query(Subject.name, Subject.code)
                    .join(Grade, Grade.id == Subject.grade_id)
                    .filter(Grade.name == assessment['grade'])
                    .all()
                    )
        custom_subjects = [AvailableSubject(
            subject=name, subject_code=code, grade=assessment['grade']) for name, code in subjects]
        assessment['subjects'] = custom_subjects

    return mark_list
