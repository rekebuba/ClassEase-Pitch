import json
from tests.test_api.factories import StudentFactory, TeacherFactory, AdminFactory
from models.grade import Grade
import pytest


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


def test_user_register_success(client, user_register_success):
    for valid_data, role in user_register_success:
        # Send a POST request to the registration endpoint
        print("the role is:", role)
        response = client.post(f'/api/v1/registration/{role}', data=valid_data)

        # Assert that the registration was successful
        assert response.status_code == 201
        assert response.json['message'] == f'{role} registered successfully!'


@pytest.mark.parametrize("create_role_based_users", [(AdminFactory, 5), (TeacherFactory, 5), (StudentFactory, 5)], indirect=True)
def test_users_log_in_success(client, create_role_based_users):
    for user in create_role_based_users:
        response = client.post('/api/v1/auth/login', json={
            'id': user.user.identification,
            'password': user.user.identification
        })

        assert response.status_code == 200
        assert 'apiKey' in response.json
        assert response.json["message"] == "logged in successfully."


@pytest.mark.parametrize("create_role_based_users", [(TeacherFactory, 1),], indirect=True)
def test_teacher_dashboard(client, users_auth_header):
    for teacher_header in users_auth_header:
        response = client.get('/api/v1/teacher/dashboard',
                              headers=teacher_header)

        assert response.status_code == 200


@pytest.mark.parametrize("create_role_based_users", [(AdminFactory, 1),], indirect=True)
def test_admin_create_semester(client, users_auth_header, event_form):
    admin_header = users_auth_header[0]

    response = client.post('/api/v1/admin/event/new',
                           json=event_form,
                           headers=admin_header,
                           content_type='application/json'
                           )

    assert response.status_code == 201
    assert response.json["message"] == "Event Created Successfully"
