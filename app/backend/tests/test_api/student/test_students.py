#!/usr/bin/python3

import pytest
from models.semester import Semester
from models.student import Student
from models.user import User
from tests.test_api.fixtures.methods import prepare_form_data
from tests.test_api.factories import StudentFactory

from flask.testing import FlaskClient

from tests.test_api.schemas.base_schema import (
    DashboardUserInfoResponseModel,
    StudentSubjectToRegister,
)
from tests.typing import Credential


class TestStudents:
    """
    tests for the student-related API endpoints.
    """

    def test_register_success(self, client: FlaskClient) -> None:
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

    def test_login_success(self, client: FlaskClient, create_student: Student) -> None:
        """
        Test the student login endpoint for successful login.
        """
        response = client.post(
            "/api/v1/auth/login",
            json={
                "id": create_student.user.identification,
                "password": create_student.user.identification,
            },
        )

        assert response.status_code == 200
        assert response.json is not None
        assert "apiKey" in response.json
        assert isinstance(response.json["apiKey"], str)
        assert len(response.json["apiKey"]) > 0

    def test_login_wrong_id(self, client: FlaskClient, create_student: Student) -> None:
        """
        Test that an invalid student ID returns an error during login.
        """
        response = client.post(
            "/api/v1/auth/login",
            json={
                "id": "wrong_id",
                "password": create_student.user.identification,
            },
        )

        assert response.status_code, 401

    def test_login_wrong_password(
        self, client: FlaskClient, create_student: Student
    ) -> None:
        """
        Test that an invalid student ID returns an error during login.
        """
        response = client.post(
            "/api/v1/auth/login",
            json={
                "id": create_student.user.identification,
                "password": "wrong_password",
            },
        )

        assert response.status_code, 401

    def test_dashboard_success(
        self, client: FlaskClient, stud_auth_header: Credential
    ) -> None:
        """
        Test the teacher dashboard endpoint for successful access.
        """
        response = client.get("/api/v1/", headers=stud_auth_header["header"])
        assert response.status_code == 200
        assert response.json is not None

        # Validate the entire response structure
        try:
            DashboardUserInfoResponseModel(**response.json)
        except Exception as e:
            pytest.fail(f"Response validation failed: {str(e)}")

    def test_available_subjects_for_registration(
        self,
        client: FlaskClient,
        semester_one_created: Semester,
        stud_auth_header: Credential,
    ) -> None:
        """
        Test the endpoint to get available subjects for registration.
        """
        response = client.get(
            "/api/v1/student/course/registration", headers=stud_auth_header["header"]
        )

        assert response.status_code == 200
        assert response.json is not None

        # Validate the entire response structure
        try:
            StudentSubjectToRegister(**response.json)
        except Exception as e:
            pytest.fail(f"Response validation failed: {str(e)}")

    def test_course_registration(
        self,
        client: FlaskClient,
        semester_one_created: Semester,
        stud_auth_header: Credential,
    ) -> None:
        """
        Test the course registration endpoint for students.
        """
        get_course = client.get(
            "/api/v1/student/course/registration", headers=stud_auth_header["header"]
        )
        assert get_course.status_code == 200
        courses = get_course.json

        response = client.post(
            "/api/v1/student/course/registration",
            json=courses,
            headers=stud_auth_header["header"],
        )

        assert response.status_code == 201
        assert response.json is not None
        assert "message" in response.json
        assert response.json["message"] == "Course registration successful!"
