#!/usr/bin/python

import time
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
from sqlalchemy import update, and_, text
from tests.test_api.helper_functions import *
from models import storage
from models.base_model import CustomTypes
from .factories_methods import MakeFactory


@pytest.fixture(scope="session")
def app_session():
    """Session-scoped fixture for the Flask app."""
    app = create_app("testing")

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


@pytest.fixture(params=[
    (CustomTypes.RoleEnum.STUDENT, 1),
    (CustomTypes.RoleEnum.ADMIN, 1),
    (CustomTypes.RoleEnum.TEACHER, 1),
])
def register_users(request, db_session):
    role, count = request.param if request.param else (None, 0)

    data = []
    role_user = None
    for _ in range(count):
        user = MakeFactory(UserFactory, db_session, built=True).factory(
            role=role)
        if role == CustomTypes.RoleEnum.STUDENT:
            current_grade = random.randint(1, 10)
            academic_year = DefaultFelids.current_EC_year()
            role_user = MakeFactory(StudentFactory, db_session, built=True).factory(
                add={"current_grade": current_grade,
                     "academic_year": academic_year}
            )
        elif role == CustomTypes.RoleEnum.TEACHER:
            role_user = MakeFactory(
                TeacherFactory, db_session, built=True).factory()
        elif role == CustomTypes.RoleEnum.ADMIN:
            role_user = MakeFactory(
                AdminFactory, db_session, built=True).factory()

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


@pytest.fixture
def db_create_users(db_session):
    factories = [
        (MakeFactory(AdminFactory, db_session).factory,
         CustomTypes.RoleEnum.ADMIN, 1),
        (MakeFactory(TeacherFactory, db_session).factory,
         CustomTypes.RoleEnum.TEACHER, 1),
        (MakeFactory(StudentFactory, db_session).factory,
         CustomTypes.RoleEnum.STUDENT, 5)
    ]

    users = {
        CustomTypes.RoleEnum.ADMIN: [],
        CustomTypes.RoleEnum.TEACHER: [],
        CustomTypes.RoleEnum.STUDENT: []
    }

    for Factory, role, count in factories:
        for _ in range(count):
            user = MakeFactory(UserFactory, db_session).factory(role=role)
            if role == CustomTypes.RoleEnum.STUDENT:
                start_year_id = db_session.query(Year.id).scalar()
                current_grade = random.randint(1, 10)
                current_grade_id = db_session.query(Grade.id).filter_by(
                    name=current_grade).scalar(),
                role_user = Factory(
                    user_id=user['id'],
                    start_year_id=start_year_id,
                    current_year_id=start_year_id,  # Assuming both are the same,
                    current_grade_id=current_grade_id,
                )
            else:
                role_user = Factory(user_id=user['id'])

            users[role].append({**user, **role_user})

    return users


@pytest.fixture
def role(request, db_session):
    role, count = request.param
    user = db_session.query(User).filter_by(
        role=role).limit(100 if count == 'all' else count).all()

    return user


@pytest.fixture
def users_auth_header(client, db_create_users, role):
    auth_headers = []
    for user in role:
        response = client.post('/api/v1/auth/login', json={
            'id': user.identification,
            'password': user.identification
        })
        token = response.json["apiKey"]
        auth_headers.append({
            "header": {
                "apiKey": f"Bearer {token}"
            },
            "user": user
        })

    return auth_headers


@pytest.fixture
def event_form(db_session):
    event = MakeFactory(EventFactory, db_session, built=True).factory(
        purpose='New Semester',
        add={'academic_year': DefaultFelids.current_EC_year()}
    )
    form = MakeFactory(SemesterFactory, db_session, built=True).factory()

    semester_form = {
        **event,
        'semester': {
            **form
        },
    }

    return semester_form


@pytest.fixture
def db_event_form(db_session):
    event = MakeFactory(EventFactory, db_session).factory(
        year_id=db_session.query(Year.id).scalar(),
        purpose='New Semester',
    )

    form = MakeFactory(SemesterFactory, db_session).factory(
        event_id=event['id'])

    return form


@pytest.fixture
def db_course_registration(db_session, db_event_form):
    students = (db_session.query(Student)
                .join(User, User.id == Student.user_id)
                .filter(User.role == CustomTypes.RoleEnum.STUDENT)
                .all()
                )

    for student in students:
        grade = (db_session.query(Grade.id)
                    .filter(Grade.id == (student.next_grade_id if student.next_grade_id else student.current_grade_id))
                    .first()
                    )
        semester = (db_session.query(Semester.id)
                       .filter_by(name=(1 if not student.next_grade_id else 2))
                       .first()
                       )

        new_semester_record = STUDSemesterRecord(
            user_id=student.user_id,
            semester_id=semester.id,
            grade_id=grade.id,
        )
        db_session.add(new_semester_record)
        db_session.flush()

        subjects = (
            db_session.query(
                Subject.name.label("subject"),
                Subject.code.label("subject_code"),
                Grade.name.label("grade")
            )
            .join(Grade, Grade.id == Subject.grade_id)
            .filter(Grade.id == grade.id)
            .all()
        )

        for subject in subjects:
            new_assessment = []
            subject_id = db_session.query(Subject.id).filter_by(
                name=subject.subject, code=subject.subject_code).scalar()

            new_assessment.append(
                Assessment(
                    user_id=student.user_id,
                    subject_id=subject_id,
                    semester_record_id=new_semester_record.id,
                )
            )

            db_session.bulk_save_objects(new_assessment)

            db_session.execute(
                update(Student)
                .where(Student.user_id == student.id)
                .values(
                    semester_id=semester.id,
                    current_grade_id=grade.id,
                    next_grade_id=None,
                    has_passed=False,
                    is_registered=True,
                    is_active=True,
                    updated_at=datetime.utcnow()
                )
            )

            db_session.commit()


@pytest.fixture
def fake_mark_list(db_session):
    # generate fake mark list for each grade
    registered_grades = (
        storage.session.query(Grade)
        .join(STUDSemesterRecord, STUDSemesterRecord.grade_id == Grade.id)
        .group_by(Grade.id)
        .all()
    )

    available_teachers = (db_session.query(User.identification)
                          .join(Teacher, User.id == Teacher.user_id)
                          .all()
                          )

    grades = {grade.name for grade in registered_grades}
    mark_list = MarkListFactory(grade_num=len(grades)).to_dict()
    mark_list.pop('grade_num')

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
