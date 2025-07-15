import pytest
from api.v1.views.shared.auth.schema import AuthResponseSchema
from api.v1.views.shared.registration.schema import SucssussfulRegistrationResponse
from extension.pydantic.models.teacher_schema import TeacherWithRelationshipsSchema
from flask.testing import FlaskClient
from models.user import User
from tests.factories.models.teacher_factory import TeacherFactory
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
        teacher = TeacherFactory.stub(
            user=None,
            teacher_records=[],
        )

        teacher_schema = TeacherWithRelationshipsSchema.model_validate(teacher)
        data = teacher_schema.model_dump(
            by_alias=True,
            exclude={
                "id",
                "user",
                "teacher_records",
            },
            exclude_none=True,
            mode="json",
        )

        # Send a POST request to the registration endpoint
        response = client.post(
            "/api/v1/teachers",
            json=data,
            content_type="application/json",
        )

        assert response.status_code == 201
        assert response.json is not None
        try:
            SucssussfulRegistrationResponse.model_validate(response.json)
        except Exception as e:
            pytest.fail(f"Response validation failed: {str(e)}")

    def test_teacher_login_success(
        self, client: FlaskClient, create_teacher: User
    ) -> None:
        """
        Test the teacher login endpoint for successful login.
        """
        response = client.post(
            "/api/v1/auth/login",
            json={
                "identification": create_teacher.identification,
                "password": create_teacher.identification,
            },
        )

        assert response.status_code == 200
        assert response.json is not None
        try:
            AuthResponseSchema.model_validate(response.json)
        except Exception as e:
            pytest.fail(f"Response validation failed: {str(e)}")

    def test_teacher_login_wrong_id(
        self, client: FlaskClient, create_teacher: User
    ) -> None:
        """
        Test that an invalid teacher ID returns an error during login.
        """
        response = client.post(
            "/api/v1/auth/login",
            json={
                "identification": "wrong_id",
                "password": create_teacher.identification,
            },
        )

        assert response.status_code, 401

    def test_admin_login_wrong_password(
        self, client: FlaskClient, create_teacher: User
    ) -> None:
        """
        Test that an invalid password returns an error during admin login.
        """
        response = client.post(
            "/api/v1/auth/login",
            json={
                "identification": create_teacher.identification,
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
