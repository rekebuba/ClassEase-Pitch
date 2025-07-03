from dataclasses import asdict
from typing import Any, Dict, Iterator, List, Optional
from flask.testing import FlaskClient
from pydantic import BaseModel
import pytest
from sqlalchemy.orm import scoped_session, Session

from models.academic_term import AcademicTerm
from tests.test_api.factories import QueryFactory
from tests.test_api.factories.academic_term_factory import AcademicTermFactory
from tests.test_api.fixtures.student_fixtures import StudentQueryResponse
from tests.typing import Credential


class AllStudentViewsResponse(BaseModel):
    viewId: str
    name: str
    tableName: str
    columns: List[str]
    searchParams: Optional[Dict[str, Any]] = None
    createdAt: str


@pytest.fixture(scope="session")
def semester_one_created(
    db_session: scoped_session[Session],
    client: FlaskClient,
) -> Iterator[AcademicTerm]:
    """
    Fixture to create the first semester for testing purposes.
    """
    yield AcademicTermFactory.get_or_create(name=1)


@pytest.fixture(scope="session")
def semester_two_created(
    db_session: scoped_session[Session],
    client: FlaskClient,
) -> Iterator[AcademicTerm]:
    """
    Fixture to create the second semester for testing purposes.
    """
    yield AcademicTermFactory.get_or_create(name=2)


@pytest.fixture(scope="session")
def admin_student_avrage_range(
    db_session: scoped_session[Session],
    client: FlaskClient,
    admin_auth_header: Credential,
) -> Iterator[Dict[str, Any]]:
    response = client.get(
        "/api/v1/admin/students/average-range",
        headers=admin_auth_header["header"],
    )

    assert response.status_code == 200
    assert response.json is not None

    yield response.json


@pytest.fixture(scope="module")
def admin_create_student_table_view(
    client: FlaskClient,
    student_query_table_data: StudentQueryResponse,
    admin_auth_header: Credential,
) -> Iterator[Credential]:
    """
    Fixture to test the saving of student table views.
    """
    table_id = dict(student_query_table_data.tableId)
    query = asdict(QueryFactory.create(tableId=table_id))
    query["search_params"].pop("sort_test_ids")

    response = client.post(
        "/api/v1/admin/views",
        json=query,
        headers=admin_auth_header["header"],
    )

    assert response.status_code == 201
    assert response.json is not None
    assert "message" in response.json
    assert response.json["message"] == "View Saved Successfully!"

    yield admin_auth_header
