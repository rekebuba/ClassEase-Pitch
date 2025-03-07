import json
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
    valid_data, role = user_register_success
    # Send a POST request to the registration endpoint
    response = client.post(f'/api/v1/registration/{role}', data=valid_data)

    # Assert that the registration was successful
    assert response.status_code == 201
    assert response.json['message'] == f'{role} registered successfully!'


# @pytest.mark.parametrize("role_factory, role", [(TeacherFactory, "teacher")])
def test_users_log_in_success(client, role_based_user):
    response = client.post('/api/v1/auth/login', json={
        'id': role_based_user.user.identification,
        'password': role_based_user.user.identification
    })

    assert response.status_code == 200
    assert 'apiKey' in response.json
    assert response.json["message"] == "logged in successfully."
