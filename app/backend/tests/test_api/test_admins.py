#!/usr/bin/python

import pytest
from models.user import User
from tests.test_api.factories import AdminFactory
from tests.test_api.fixtures.methods import prepare_form_data
from flask.testing import FlaskClient


class TestAdmin:
    """
    TestAdmin is a test suite for testing the admin-related endpoints of the API.
    """

    def test_admin_register_success(self, client: FlaskClient) -> None:
        """
        Test the successful registration of an admin.
        """
        admin = AdminFactory.build()
        form_data = prepare_form_data(admin)

        # Send a POST request to the registration endpoint
        response = client.post(
            f"/api/v1/registration/{admin['user']['role']}",
            data=form_data,
        )

        assert response.status_code == 201
        assert response.json is not None
        assert "message" in response.json
        assert response.json["message"] == "admin registered successfully!"

    def test_admin_login_success(
        self, client: FlaskClient, register_admin: None, random_admin: User
    ) -> None:
        """
        Test the admin login endpoint for successful login.
        """

        response = client.post(
            "/api/v1/auth/login",
            json={
                "id": random_admin.identification,
                "password": random_admin.identification,
            },
        )

        assert response.status_code == 200
        assert response.json is not None
        assert "apiKey" in response.json
        assert isinstance(response.json["apiKey"], str)
        assert len(response.json["apiKey"]) > 0

    def test_admin_login_wrong_id(
        self, client: FlaskClient, register_admin: None, random_admin: User
    ) -> None:
        """
        Test that an invalid admin login returns an error.
        """
        response = client.post(
            "/api/v1/auth/login",
            json={
                "id": "wrong_id",
                "password": random_admin.identification,
            },
        )

        assert response.status_code, 401

    def test_admin_login_wrong_password(
        self, client: FlaskClient, register_admin: None, random_admin: User
    ) -> None:
        """
        Test the admin login functionality with an incorrect password.
        """
        response = client.post(
            "/api/v1/auth/login",
            json={
                "id": random_admin.identification,
                "password": "wrong_password",
            },
        )

        assert response.status_code, 401

    def test_admin_dashboard_success(self):
        """
        Test the admin dashboard access with a valid login.
        """
        pytest.skip("Skipping test for not implemented endpoint")

    def test_admin_dashboard_failure(self):
        """
        Test the admin dashboard access with an invalid token.
        """
        pytest.skip("Skipping test for not implemented endpoint")

    def test_admin_create_mark_list(self):
        """
        Test the creation of a mark list by an admin.
        """
        pytest.skip("Skipping test for not implemented endpoint")

    def test_admin_create_mark_list_failure(self):
        """
        Test case for creating a mark list with invalid token.
        """
        pytest.skip("Skipping test for not implemented endpoint")

    def test_view_admin_mark_list(self):
        """
        Test that an admin can view the mark list for students.
        """
        pytest.skip("Skipping test for not implemented endpoint")

    def test_admin_access_to_teacher_data(self):
        """
        Test that an admin can access teacher data.
        """
        pytest.skip("Skipping test for not implemented endpoint")

    def test_admin_access_to_teacher_data_failure(self):
        """
        Test case to verify that an admin cannot access teacher data with an invalid token.
        """
        pytest.skip("Skipping test for not implemented endpoint")

    def test_admin_course_assign_to_teacher(self):
        """
        Test case for assigning a course to a teacher by an admin.
        """
        pytest.skip("Skipping test for not implemented endpoint")

    def test_admin_course_assign_to_teacher_failure(self):
        """
        Test that an admin cannot assign a non-existent subject to a teacher.
        """
        pytest.skip("Skipping test for not implemented endpoint")
