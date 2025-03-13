from datetime import date, datetime
import json
import pytest
from tests.test_api.factories import StudentFactory, TeacherFactory, AdminFactory
from models.user import User
from models.year import Year
from models.subject import Subject
from models.student import Student
from models.grade import Grade
from models.event import Event
from models.assessment import Assessment
from models.stud_semester_record import STUDSemesterRecord


def test_db_grade_count(client, db_session):
    # Query the database
    grade_count = db_session.query(Grade).count()

    # Assert that the database has the correct number of grades
    assert grade_count == 12


def test_db_grade_values(client, db_session):
    # Query the database
    grades = db_session.query(Grade.name).order_by(Grade.name).all()
    grade_values = [grade.name for grade in grades]

    # Assert that the database has the correct grade values
    assert grade_values == list(range(1, 13))


def test_db_subject_count(client, db_session):
    # Query the database
    subject = db_session.query(Subject).count()
    assert subject > 0


def test_db_year_count(client, db_session):
    # Query the database
    year = db_session.query(Year).count()
    assert year > 0


def test_user_register_success(client, user_register_success):
    for valid_data, role in user_register_success:
        # Send a POST request to the registration endpoint
        response = client.post(f'/api/v1/registration/{role}', data=valid_data)

        # Assert that the registration was successful
        assert response.status_code == 201
        assert response.json['message'] == f'{role} registered successfully!'


def test_users_log_in_success(client, db_create_users):
    for user in db_create_users:
        response = client.post('/api/v1/auth/login', json={
            'id': user.user.identification,
            'password': user.user.identification
        })

        assert response.status_code == 200
        assert 'apiKey' in response.json
        assert response.json["message"] == "logged in successfully."


@pytest.mark.parametrize("role", ['teacher'], indirect=True)
def test_teacher_dashboard(client, db_create_users, users_auth_header):
    response = client.get('/api/v1/teacher/dashboard',
                          headers=users_auth_header)

    assert response.status_code == 200


@pytest.mark.parametrize("role", ['admin'], indirect=True)
def test_admin_create_semester(client, db_create_users, users_auth_header, event_form):

    response = client.post('/api/v1/admin/event/new',
                           json=event_form,
                           headers=users_auth_header
                           )

    assert response.status_code == 201
    assert response.json["message"] == "Event Created Successfully"


@pytest.mark.parametrize("role", ['student'], indirect=True)
def test_student_subjects_for_registration(client, db_create_users, db_event_form, users_auth_header):
    response = client.get('/api/v1/student/course/registration',
                          headers=users_auth_header
                          )
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert len(response.json) > 0


@pytest.mark.parametrize("role", ['student'], indirect=True)
def test_student_course_registration(client, db_create_users, db_event_form, users_auth_header, course_registration):
    response = client.post('/api/v1/student/course/registration',
                           json=course_registration,
                           headers=users_auth_header
                           )

    assert response.status_code == 201
    assert response.json['message'] == 'Course registration successful!'


@pytest.mark.parametrize("role", ['admin'], indirect=True)
def test_admin_create_mark_list(client, db_session, db_create_users, db_event_form, users_auth_header, db_course_registration, fake_mark_list):
    pass
