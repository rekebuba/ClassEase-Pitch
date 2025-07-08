from typing import List
from flask.testing import FlaskClient
import pytest
from pydantic import TypeAdapter, ValidationError

from extension.pydantic.models.grade_schema import GradeSchema
from extension.pydantic.models.subject_schema import SubjectSchema


@pytest.fixture
def subjects(client: FlaskClient) -> List[SubjectSchema]:
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
def grades(client: FlaskClient) -> List[GradeSchema]:
    response = client.get("/api/v1/grades")

    assert response.status_code == 200
    assert response.json is not None
    assert isinstance(response.json, list)
    assert len(response.json) > 0
    try:
        grades = TypeAdapter(list[GradeSchema]).validate_python(response.json)
        return grades
    except ValidationError as e:
        pytest.fail(f"Validation error: {e}")
