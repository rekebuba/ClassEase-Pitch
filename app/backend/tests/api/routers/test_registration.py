import random
from typing import Dict

import pytest
from fastapi.testclient import TestClient

from project.api.v1.routers.registrations.schema import RegistrationResponse
from project.core.config import settings
from project.models.parent import Parent
from project.models.year import Year
from project.utils.enum import EmployeePositionEnum
from tests.factories.api_data import (
    AdminRegistrationFactory,
    EmployeeRegistrationFactory,
    ParentRegistrationFactory,
    StudentRegistrationFactory,
)


class TestRegistration:
    def test_admin_registration(
        self,
        client: TestClient,
        admin_token_headers: Dict[str, str],
    ) -> None:
        """Test Admin Registration"""

        admin_data = AdminRegistrationFactory.build()

        r = client.post(
            f"{settings.API_V1_STR}/register/admins",
            json=admin_data.model_dump(mode="json", by_alias=True),
            headers=admin_token_headers,
        )

        assert r.status_code == 201

        result = RegistrationResponse.model_validate_json(r.text)

        assert "Admin Registered Successfully" == result.message
        assert result.id is not None

    def test_parent_registration(
        self,
        client: TestClient,
        admin_token_headers: Dict[str, str],
    ) -> None:
        """Test Parent Registration"""

        parent = ParentRegistrationFactory.build()

        r = client.post(
            f"{settings.API_V1_STR}/register/parents",
            json=parent.model_dump(mode="json", by_alias=True),
            headers=admin_token_headers,
        )

        assert r.status_code == 201

        result = RegistrationResponse.model_validate_json(r.text)

        assert "Parent Registered Successfully" == result.message
        assert result.id is not None

    def test_student_registration(
        self,
        client: TestClient,
        admin_token_headers: Dict[str, str],
        year: Year,
        parent: Parent,
    ) -> None:
        """Test Student Registration"""

        grade = random.choice(year.grades)
        student = StudentRegistrationFactory.build(
            registered_for_grade_id=grade.id, parent_id=parent.id
        )

        r = client.post(
            f"{settings.API_V1_STR}/register/students",
            json=student.model_dump(
                mode="json",
                by_alias=True,
            ),
            headers=admin_token_headers,
        )

        assert r.status_code == 201

        result = RegistrationResponse.model_validate_json(r.text)

        assert "Student Registered Successfully" == result.message
        assert result.id is not None

    @pytest.mark.parametrize(
        "position",
        [EmployeePositionEnum.TEACHING_STAFF] * 2,
    )
    def test_employee_registration(
        self,
        client: TestClient,
        admin_token_headers: Dict[str, str],
        year: Year,
        position: EmployeePositionEnum,
    ) -> None:
        """Test Employee Registration"""

        subject = random.choice(year.subjects)
        employee = EmployeeRegistrationFactory.build(
            position=position, subject_id=subject.id
        )

        r = client.post(
            f"{settings.API_V1_STR}/register/employees",
            json=employee.model_dump(mode="json", by_alias=True),
            headers=admin_token_headers,
        )

        assert r.status_code == 201

        result = RegistrationResponse.model_validate_json(r.text)
        assert "Employee Registered Successfully" == result.message
        assert result.id is not None
