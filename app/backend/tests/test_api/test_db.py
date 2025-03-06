import json
from models.grade import Grade
from contextlib import contextmanager
import pytest
from tests.test_api.factories import *


def test_db_grade_count(client, db_session):
    # Query the database
    grade_count = db_session.query(Grade).count()

    # Assert that the database has the correct number of grades
    assert grade_count == 12


def test_db_grade_values(client, db_session):
    # Query the database
    grades = db_session.query(Grade.grade).order_by(Grade.grade).all()
    grade_values = [grade.grade for grade in grades]

    # Assert that the database has the correct grade values
    assert grade_values == list(range(1, 13))


@contextmanager
def override_session(factory, session):
    """Temporarily override the sqlalchemy_session in a factory."""
    original_session = factory._meta.sqlalchemy_session
    factory._meta.sqlalchemy_session = session
    try:
        yield
    finally:
        factory._meta.sqlalchemy_session = original_session


# @pytest.fixture(params=[(AdminFactory, 'admin'), (StudentFactory, 'student'), (TeacherFactory, 'teacher')])
def test_admin_register_success(client, db_session):
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

    # Assert that the registration was successful
    assert response.status_code == 201
    assert response.json['message'] == 'admin registered successfully!'


def test_student_register_success(client, db_session):
    with override_session(StudentFactory, db_session):
        student = StudentFactory()

        # Convert the student object to a dictionary
        student_data = student.to_dict()

        student_data.pop('id')
        student_data.pop('created_at')
        student_data.pop('updated_at')
        student_data.pop('__class__')
        student_data.pop('semester_id')

        print(json.dumps(student_data, indent=4, sort_keys=True))

        # Send a POST request to the registration endpoint
        response = client.post('/api/v1/registration/student',
                               data=student_data)

    # Assert that the registration was successful
    assert response.json['message'] == 'student registered successfully!'
    assert response.status_code == 201
