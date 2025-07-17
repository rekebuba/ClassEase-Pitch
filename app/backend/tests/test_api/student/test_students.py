#!/usr/bin/python3

import pytest
from api.v1.views.shared.auth.schema import AuthResponseSchema
from api.v1.views.shared.registration.schema import RegistrationResponse
from extension.pydantic.models.student_schema import (
    StudentSchema,
    StudentWithRelationshipsSchema,
)
from extension.pydantic.response.schema import SuccessResponseSchema
from models.academic_term import AcademicTerm
from models.user import User
from tests.factories.models import StudentFactory

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
        student = StudentFactory.build(
            user=None,
            student_year_records=[],
        )
        # form_data = prepare_form_data(student)
        student_schema = StudentSchema.model_validate(student)
        data = student_schema.model_dump(
            by_alias=True,
            exclude={
                "id",
                "user_id",
                "student_year_records",
            },
            exclude_none=True,
            mode="json",
        )
        # Send a POST request to the registration endpoint
        response = client.post(
            "/api/v1/students",
            json=data,
            content_type="application/json",
        )

        assert response.status_code == 201
        assert response.json is not None
        # Validate the response structure
        try:
            SuccessResponseSchema[RegistrationResponse, None, None].model_validate(
                response.json
            )
        except Exception as e:
            pytest.fail(f"Response validation failed: {str(e)}")

    def test_login_success(self, client: FlaskClient, create_student: User) -> None:
        """
        Test the student login endpoint for successful login.
        """
        response = client.post(
            "/api/v1/auth/login",
            json={
                "identification": create_student.identification,
                "password": create_student.identification,
            },
        )

        assert response.status_code == 200
        assert response.json is not None
        try:
            AuthResponseSchema.model_validate(response.json)
        except Exception as e:
            pytest.fail(f"Response validation failed: {str(e)}")

    def test_login_wrong_id(self, client: FlaskClient, create_student: User) -> None:
        """
        Test that an invalid student ID returns an error during login.
        """
        response = client.post(
            "/api/v1/auth/login",
            json={
                "identification": "wrong_id",
                "password": create_student.identification,
            },
        )

        assert response.status_code, 401

    def test_login_wrong_password(
        self,
        client: FlaskClient,
        create_student: User,
    ) -> None:
        """
        Test that an invalid student ID returns an error during login.
        """
        response = client.post(
            "/api/v1/auth/login",
            json={
                "identification": create_student.identification,
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
        semester_one_created: AcademicTerm,
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
        semester_one_created: AcademicTerm,
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
