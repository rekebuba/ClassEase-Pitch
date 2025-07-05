import json
import random
import pytest
from sqlalchemy import select
from sqlmodel import col

from models.grade import Grade
from models.teacher import Teacher
from tests.test_api.factories import TeacherFactory
from flask.testing import FlaskClient
from tests.test_api.factories.year_factory import YearFactory
from tests.test_api.schemas.base_schema import DashboardUserInfoResponseModel
from tests.typing import Credential


class TestTeachers:
    """
    TestTeachers is a test case class for testing the teacher-related endpoints of the API.
    """

    def test_teacher_register_success(self, client: FlaskClient) -> None:
        """
        Test the successful registration of a teacher.
        """

        # form_data = prepare_form_data(teacher)
        YearFactory.create()
        teacher = TeacherFactory.create(user=None, for_session=True)

        # teacher.pop("user", None)
        # # Send a POST request to the registration endpoint
        # response = client.post(
        #     "/api/v1/register/teacher",
        #     json=teacher,
        # )

        # assert response.status_code == 201
        # assert response.json is not None
        # assert "message" in response.json
        # assert response.json["message"] == "teacher registered successfully!"

    def test_teacher_login_success(
        self, client: FlaskClient, create_teacher: Teacher
    ) -> None:
        """
        Test the teacher login endpoint for successful login.
        """
        response = client.post(
            "/api/v1/auth/login",
            json={
                "id": create_teacher.user.identification,
                "password": create_teacher.user.identification,
            },
        )

        assert response.status_code == 200
        assert response.json is not None
        assert "apiKey" in response.json
        assert isinstance(response.json["apiKey"], str)
        assert len(response.json["apiKey"]) > 0

    def test_teacher_login_wrong_id(
        self, client: FlaskClient, create_teacher: Teacher
    ) -> None:
        """
        Test that an invalid teacher ID returns an error during login.
        """
        response = client.post(
            "/api/v1/auth/login",
            json={
                "id": "wrong_id",
                "password": create_teacher.user.identification,
            },
        )

        assert response.status_code, 401

    def test_admin_login_wrong_password(
        self, client: FlaskClient, create_teacher: Teacher
    ) -> None:
        """
        Test that an invalid password returns an error during admin login.
        """
        response = client.post(
            "/api/v1/auth/login",
            json={
                "id": create_teacher.user.identification,
                "password": "wrong_password",
            },
        )

        assert response.status_code, 401

    def test_teacher_dashboard_success(
        self, client: FlaskClient, teacher_auth_header: Credential
    ) -> None:
        """
        Test the teacher dashboard endpoint for successful access.
        """
        response = client.get("/api/v1/", headers=teacher_auth_header["header"])

        assert response.status_code == 200
        assert response.json is not None

        # Validate the entire response structure
        try:
            DashboardUserInfoResponseModel(**response.json)
        except Exception as e:
            pytest.fail(f"Response validation failed: {str(e)}")

    def test_get_teacher_assigned_grade_success(self):
        """
        Test the successful retrieval of a teacher's assigned grade.
        """
        pass

    def test_get_teacher_assigned_grade_no_grades(self):
        """
        Test the get_teacher_assigned_grade endpoint when no grades are assigned to a teacher.
        """
        pass
