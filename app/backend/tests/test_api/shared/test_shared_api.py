from pydantic import TypeAdapter, ValidationError
import pytest


class TestSharedApi:
    def test_get_subjects(self, client):
        response = client.get("/api/v1/available-subjects")

        assert response.status_code == 200
        assert response.json is not None
        try:
            subjects = TypeAdapter(list[str]).validate_python(response.json)
            assert isinstance(subjects, list)
        except ValidationError as e:
            pytest.fail(f"Validation error: {e}")

    def test_get_grades(self, client):
        response = client.get("/api/v1/available-grades")

        assert response.status_code == 200
        assert response.json is not None
        try:
            grades = TypeAdapter(list[int]).validate_python(response.json)
            assert isinstance(grades, list)
        except ValidationError as e:
            pytest.fail(f"Validation error: {e}")
