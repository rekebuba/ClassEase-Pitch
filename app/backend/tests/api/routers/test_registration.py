import random
from typing import Dict

from fastapi.testclient import TestClient

from core.config import settings
from models.year import Year
from tests.factories.api_data import (
    EmployeeRegistrationFactory,
    StudentRegistrationFactory,
)
from utils.enum import EmployeePositionEnum


class TestRegistration:
    def test_student_registration(
        self,
        client: TestClient,
        admin_token_headers: Dict[str, str],
        year: Year,
    ) -> None:
        """Test Student Registration"""

        grade = random.choice(year.grades)
        student = StudentRegistrationFactory.create(registered_for_grade_id=grade.id)

        r = client.post(
            f"{settings.API_V1_STR}/register/students",
            json=student.model_dump(mode="json", by_alias=True),
            headers=admin_token_headers,
        )

        assert r.status_code == 201
        assert r.json() is not None
        assert r.json().get("message") == "Student Registered Successfully"
        assert r.json().get("id") is not None

    def test_employee_registration(
        self,
        client: TestClient,
        admin_token_headers: Dict[str, str],
        year: Year,
    ) -> None:
        """Test Student Registration"""

        subject = random.choice(year.subjects)
        employee = EmployeeRegistrationFactory.create(
            position=EmployeePositionEnum.TEACHING_STAFF, subject_id=subject.id
        )

        r = client.post(
            f"{settings.API_V1_STR}/register/employees",
            json=employee.model_dump(mode="json", by_alias=True),
            headers=admin_token_headers,
        )

        assert r.status_code == 201
        assert r.json() is not None
        assert r.json().get("message") == "Employee Registered Successfully"
        assert r.json().get("id") is not None
