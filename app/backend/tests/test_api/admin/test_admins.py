#!/usr/bin/python

from typing import Any, Dict
from pydantic import TypeAdapter
import pytest
from models.admin import Admin
from tests.test_api.factories import AdminFactory, EventFactory
from tests.test_api.fixtures.methods import prepare_form_data
from flask.testing import FlaskClient

from tests.test_api.schemas.base_schema import (
    AverageRangeResponseModel,
    DashboardUserInfoResponseModel,
    RegisteredGradeResponseModel,
    SectionCountResponseModel,
)
from tests.typing import Credential


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
        self, client: FlaskClient, create_admin: Admin
    ) -> None:
        """
        Test the admin login endpoint for successful login.
        """

        response = client.post(
            "/api/v1/auth/login",
            json={
                "id": create_admin.user.identification,
                "password": create_admin.user.identification,
            },
        )

        assert response.status_code == 200
        assert response.json is not None
        assert "apiKey" in response.json
        assert isinstance(response.json["apiKey"], str)
        assert len(response.json["apiKey"]) > 0

    def test_admin_login_wrong_id(
        self, client: FlaskClient, create_admin: Admin
    ) -> None:
        """
        Test that an invalid admin login returns an error.
        """
        response = client.post(
            "/api/v1/auth/login",
            json={
                "id": "wrong_id",
                "password": create_admin.user.identification,
            },
        )

        assert response.status_code, 401

    def test_admin_login_wrong_password(
        self, client: FlaskClient, create_admin: Admin
    ) -> None:
        """
        Test the admin login functionality with an incorrect password.
        """
        response = client.post(
            "/api/v1/auth/login",
            json={
                "id": create_admin.user.identification,
                "password": "wrong_password",
            },
        )

        assert response.status_code, 401

    def test_admin_dashboard_success(
        self, client: FlaskClient, admin_auth_header: Credential
    ) -> None:
        """
        Test the admin dashboard access with a valid login.
        """
        response = client.get("/api/v1/", headers=admin_auth_header["header"])
        assert response.status_code == 200
        assert response.json is not None

        # Validate the entire response structure
        try:
            DashboardUserInfoResponseModel(**response.json)
        except Exception as e:
            pytest.fail(f"Response validation failed: {str(e)}")

    def test_new_event_for_semster(
        self, client: FlaskClient, admin_auth_header: Credential
    ) -> None:
        """
        Test the creation of a new event for a semester.
        """
        event_form = EventFactory.build(purpose="New Semester")

        response = client.post(
            "/api/v1/admin/event/new",
            json=event_form,
            headers=admin_auth_header["header"],
        )
        assert response.status_code == 201
        assert response.json is not None
        assert "message" in response.json
        assert response.json["message"] == "Event Created Successfully"

    def test_registered_grades_for_mark_list_creation(
        self,
        client: FlaskClient,
        stud_registerd_for_semester_one_course: None,
        admin_auth_header: Credential,
    ) -> None:
        """
        Test the retrieval of registered grades for mark list creation.
        """
        response = client.get(
            "/api/v1/admin/registered_grades",
            headers=admin_auth_header["header"],
        )
        assert response.status_code == 200
        assert response.json is not None

        # Validate the entire response structure
        try:
            RegisteredGradeResponseModel(**response.json)
        except Exception as e:
            pytest.fail(f"Response validation failed: {str(e)}")

    def test_mark_list_creation(
        self,
        client: FlaskClient,
        stud_registerd_for_semester_one_course: None,
        fake_mark_list: Dict[str, Any],
        admin_auth_header: Credential,
    ) -> None:
        """
        Test the creation of a mark list by an admin.
        """
        response = client.post(
            "/api/v1/admin/mark-list/new",
            json=fake_mark_list,
            headers=admin_auth_header["header"],
        )
        assert response.status_code == 201
        assert response.json is not None
        assert "message" in response.json
        assert response.json["message"] == "Mark list created successfully!"

    def test_student_grade_counts(
        self, client: FlaskClient, admin_auth_header: Credential
    ) -> None:
        """
        Test the retrieval of student section counts.
        """
        response = client.get(
            "/api/v1/admin/students/grade-counts",
            headers=admin_auth_header["header"],
        )
        assert response.status_code == 200
        assert response.json is not None

        DataValidator = TypeAdapter(Dict[str, int])

        # Validate the entire response structure
        try:
            DataValidator.validate_python(response.json)
        except Exception as e:
            pytest.fail(f"Response validation failed: {str(e)}")

    def test_student_section_counts(
        self, client: FlaskClient, admin_auth_header: Credential
    ) -> None:
        """
        Test the retrieval of student section counts.
        """
        response = client.get(
            "/api/v1/admin/students/section-counts",
            headers=admin_auth_header["header"],
        )
        assert response.status_code == 200
        assert response.json is not None

        # Validate the entire response structure
        try:
            SectionCountResponseModel(**response.json)
        except Exception as e:
            pytest.fail(f"Response validation failed: {str(e)}")

    def test_admin_student_avrage_range(
        self, client: FlaskClient, admin_auth_header: Credential
    ) -> None:
        """
        Test the retrieval of student average min and max range.
        """
        response = client.get(
            "/api/v1/admin/students/average-range",
            headers=admin_auth_header["header"],
        )
        assert response.status_code == 200
        assert response.json is not None

        # Validate the entire response structure
        try:
            AverageRangeResponseModel(**response.json)
        except Exception as e:
            pytest.fail(f"Response validation failed: {str(e)}")
