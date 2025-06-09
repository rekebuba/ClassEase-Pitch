#!/usr/bin/python3

from models.user import User
from tests.test_api.fixtures.methods import prepare_form_data
from tests.test_api.factories import StudentFactory

from flask.testing import FlaskClient


class TestStudents:
    """
    tests for the student-related API endpoints.
    """

    def test_student_register_success(self, client: FlaskClient) -> None:
        """
        Test the student registration endpoint for successful registration.
        """
        student = StudentFactory.build()
        form_data = prepare_form_data(student)

        # Send a POST request to the registration endpoint
        response = client.post(
            f"/api/v1/registration/{student['user']['role']}",
            data=form_data,
        )

        assert response.status_code == 201
        assert response.json is not None
        assert "message" in response.json
        assert response.json["message"] == "student registered successfully!"

    def test_student_login_success(
        self, client: FlaskClient, register_student: None, random_student: User
    ) -> None:
        """
        Test the student login endpoint for successful login.
        """
        response = client.post(
            "/api/v1/auth/login",
            json={
                "id": random_student.identification,
                "password": random_student.identification,
            },
        )

        assert response.status_code == 200
        assert response.json is not None
        assert "apiKey" in response.json
        assert isinstance(response.json["apiKey"], str)
        assert len(response.json["apiKey"]) > 0

    def test_student_login_wrong_id(
        self, client: FlaskClient, register_student: None, random_student: User
    ) -> None:
        """
        Test that an invalid student ID returns an error during login.
        """
        response = client.post(
            "/api/v1/auth/login",
            json={
                "id": "wrong_id",
                "password": random_student.identification,
            },
        )

        assert response.status_code, 401

    def test_student_login_wrong_password(
        self, client: FlaskClient, register_student: None, random_student: User
    ) -> None:
        """
        Test that an invalid student ID returns an error during login.
        """
        response = client.post(
            "/api/v1/auth/login",
            json={
                "id": random_student.identification,
                "password": "wrong_password",
            },
        )

        assert response.status_code, 401
