import json
import random
from typing import List
from flask.testing import FlaskClient
from pydantic import TypeAdapter, ValidationError
import pytest

from extension.pydantic.models.grade_schema import GradeSchema
from extension.pydantic.models.subject_schema import SubjectSchema
from extension.pydantic.models.year_schema import YearSchema


class TestSharedApi:
    def test_get_subjects(self, client: FlaskClient) -> None:
        """Test the API endpoint for retrieving all subjects."""
        response = client.get("/api/v1/subjects")

        assert response.status_code == 200
        assert response.json is not None
        assert isinstance(response.json, list)
        assert len(response.json) > 0
        try:
            TypeAdapter(list[SubjectSchema]).validate_python(response.json)
        except ValidationError as e:
            pytest.fail(f"Validation error: {e}")

    def test_get_subject_by_id(
        self, client: FlaskClient, subjects: List[SubjectSchema]
    ) -> None:
        """Test the API endpoint for retrieving a subject by its ID."""
        response = client.get(f"api/v1/subjects/{random.choice(subjects).id}")

        assert response.status_code == 200
        assert response.json is not None
        assert isinstance(response.json, dict)
        try:
            TypeAdapter(SubjectSchema).validate_python(response.json)
        except ValidationError as e:
            pytest.fail(f"Validation error: {e}")

    def test_get_grades(self, client: FlaskClient) -> None:
        """Test the API endpoint for retrieving all grades."""
        response = client.get("/api/v1/grades")

        assert response.status_code == 200
        assert response.json is not None
        assert isinstance(response.json, list)
        assert len(response.json) > 0
        try:
            TypeAdapter(List[GradeSchema]).validate_python(response.json)
        except ValidationError as e:
            pytest.fail(f"Validation error: {e}")

    def test_get_grade_by_id(
        self, client: FlaskClient, grades: List[GradeSchema]
    ) -> None:
        response = client.get(f"api/v1/grades/{random.choice(grades).id}")

        assert response.status_code == 200
        assert response.json is not None
        assert isinstance(response.json, dict)
        try:
            TypeAdapter(GradeSchema).validate_python(response.json)
        except ValidationError as e:
            pytest.fail(f"Validation error: {e}")

    def test_get_subject_grades(
        self, client: FlaskClient, subjects: List[SubjectSchema]
    ) -> None:
        """Test getting grades for a specific subject."""
        response = client.get(f"/api/v1/subjects/{random.choice(subjects).id}/grades")

        assert response.status_code == 200
        assert response.json is not None
        assert isinstance(response.json, list)
        assert len(response.json) > 0
        try:
            TypeAdapter(List[GradeSchema]).validate_python(response.json)
        except ValidationError as e:
            pytest.fail(f"Validation error: {e}")

    def test_get_academic_years(self, client: FlaskClient) -> None:
        """Test getting all available academic years."""
        response = client.get("/api/v1/academic_years")

        assert response.status_code == 200
        assert response.json is not None
        assert isinstance(response.json, list)
        assert len(response.json) > 0
        try:
            TypeAdapter(List[YearSchema]).validate_python(response.json)
        except ValidationError as e:
            pytest.fail(f"Validation error: {e}")
