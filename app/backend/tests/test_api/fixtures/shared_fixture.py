from typing import List
from flask.testing import FlaskClient
import pytest
from pydantic import TypeAdapter, ValidationError

from extension.pydantic.models.subject_schema import SubjectSchema


@pytest.fixture
def subject_list(client: FlaskClient) -> List[str]:
    response = client.get("/api/v1/subjects")
    assert response.status_code == 200
    assert response.json is not None
    assert isinstance(response.json, list)
    assert len(response.json) > 0
    try:
        subjects = TypeAdapter(list[SubjectSchema]).validate_python(response.json)
        return subjects
    except ValidationError as e:
        pytest.fail(f"Validation error: {e}")


@pytest.fixture
def grade_list(client: FlaskClient) -> List[str]:
    response = client.get("/api/v1/grades")

    assert response.status_code == 200
    assert response.json is not None
    assert isinstance(response.json, list)
    assert len(response.json) > 0
    try:
        grades = TypeAdapter(list[str]).validate_python(response.json)
        return grades
    except ValidationError as e:
        pytest.fail(f"Validation error: {e}")
