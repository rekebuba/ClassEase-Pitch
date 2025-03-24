from datetime import date, datetime
import json
import pytest
from models.admin import Admin
from tests.test_api.factories import StudentFactory, TeacherFactory, AdminFactory
from models.user import User
from models.year import Year
from models.subject import Subject
from models.student import Student
from models.grade import Grade
from models.event import Event
from models.assessment import Assessment
from models.mark_list import MarkList
from models.stud_semester_record import STUDSemesterRecord
from models.base_model import CustomTypes


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


def test_user_register_success(client, register_users):
    for valid_data in register_users:
        # Send a POST request to the registration endpoint
        response = client.post(
            f'/api/v1/registration/{valid_data["role"]}', data=valid_data)

        # Assert that the registration was successful
        assert response.status_code == 201
        assert response.json['message'] == f'{valid_data["role"]} registered successfully!'


def test_users_log_in_success(client, db_create_users):
    for role in db_create_users.keys():
        user = db_create_users[role]
        response = client.post('/api/v1/auth/login', json={
            'id': user[0]['identification'],
            'password': user[0]['identification']
        })

        assert response.status_code == 200
        assert 'apiKey' in response.json
        assert response.json["message"] == "logged in successfully."


@pytest.mark.parametrize("role", [(CustomTypes.RoleEnum.TEACHER, 'all'),], indirect=True)
def test_teacher_dashboard(client, users_auth_header):
    for auth_header in users_auth_header:
        response = client.get('/api/v1/teacher/dashboard',
                              headers=auth_header['header']
                              )

        assert response.status_code == 200


@pytest.mark.parametrize("role", [(CustomTypes.RoleEnum.ADMIN, 1),], indirect=True)
def test_admin_create_semester(client, users_auth_header, event_form):
    response = client.post('/api/v1/admin/event/new',
                           json=event_form,
                           headers=users_auth_header[0]['header']
                           )

    assert response.status_code == 201
    assert response.json["message"] == "Event Created Successfully"


@pytest.mark.parametrize("role", [(CustomTypes.RoleEnum.STUDENT, 1),], indirect=True)
def test_available_subjects_for_registration(client, users_auth_header, db_event_form):
    for auth_header in users_auth_header:
        response = client.get('/api/v1/student/course/registration',
                              headers=auth_header['header']
                              )
        assert response.status_code == 200
        assert isinstance(response.json, dict)
        assert len(response.json) > 0


@pytest.mark.parametrize("role", [('student', 'all'),], indirect=True)
def test_student_course_registration(client, db_session, db_event_form, users_auth_header):
    for auth_header in users_auth_header:
        student = (db_session.query(Student)
                   .join(User, User.id == Student.user_id)
                   .filter(User.identification == auth_header['user'].identification)
                   .first()
                   )

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

        subject_list = [{key: value for key, value in q._asdict().items()}
                        for q in subjects]

        courses = {"course": subject_list, "semester": 1,
                   "academic_year": 2017, "grade": subject_list[0]['grade']}

        response = client.post('/api/v1/student/course/registration',
                               json=courses,
                               headers=auth_header['header']
                               )

        # Debugging failed cases
        if response.status_code != 201:
            print(f"Failed for: {courses}")
            print(f"Response: {response.json}")

        assert response.status_code == 201
        assert response.json['message'] == 'Course registration successful!'


@pytest.mark.parametrize("role", [(CustomTypes.RoleEnum.ADMIN, 1),], indirect=True)
def test_admin_create_mark_list(client, db_session, db_create_users, event_form, users_auth_header, db_course_registration, fake_mark_list):
    # db_session.commit()

    response = client.post('/api/v1/admin/mark-list/new',
                           json=fake_mark_list,
                           headers=users_auth_header[0]['header']
                           )

    assert response.status_code == 201
    assert response.json['message'] == 'Mark list created successfully!'
