import json
import random
from typing import List
from flask.testing import FlaskClient
from pydantic import TypeAdapter, ValidationError
import pytest

from extension.pydantic.models.grade_schema import GradeSchema
from extension.pydantic.models.subject_schema import SubjectSchema


class TestSharedApi:
    def test_get_subjects(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/subjects")

        assert response.status_code == 200
        assert response.json is not None
        assert isinstance(response.json, list)
        assert len(response.json) > 0
        try:
            TypeAdapter(list[SubjectSchema]).validate_python(response.json)
        except ValidationError as e:
            pytest.fail(f"Validation error: {e}")

    def test_get_grades(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/grades")

        assert response.status_code == 200
        assert response.json is not None
        assert isinstance(response.json, list)
        assert len(response.json) > 0
        print(json.dumps(response.json, indent=2))
        try:
            TypeAdapter(List[GradeSchema]).validate_python(response.json)
        except ValidationError as e:
            pytest.fail(f"Validation error: {e}")

    def test_get_subject_grades(self, client, subject_list):
        subject_names = random.sample(
            subject_list, k=random.randint(0, len(subject_list))
        )
        response = client.get(
            "/api/v1/subjects/grades", json={"subjects": subject_names}
        )

        assert response.status_code == 200
        assert response.json is not None
        assert isinstance(response.json, list)
        assert len(response.json) > 0
        try:
            TypeAdapter(List[GradeSchema]).validate_python(response.json)
        except ValidationError as e:
            pytest.fail(f"Validation error: {e}")
