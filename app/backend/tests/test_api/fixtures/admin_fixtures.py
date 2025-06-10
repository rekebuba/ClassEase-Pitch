from typing import Any, Dict, Iterator
from flask.testing import FlaskClient
import pytest
from sqlalchemy.orm import scoped_session, Session

from models.semester import Semester
from tests.test_api.factories import SemesterFactory
from tests.typing import Credential


@pytest.fixture(scope="session")
def semester_one_created(
    db_session: scoped_session[Session],
    client: FlaskClient,
) -> Iterator[Semester]:
    """
    Fixture to create the first semester for testing purposes.
    """
    yield SemesterFactory.get_or_create(name=1)


@pytest.fixture(scope="session")
def semester_two_created(
    db_session: scoped_session[Session],
    client: FlaskClient,
) -> Iterator[Semester]:
    """
    Fixture to create the second semester for testing purposes.
    """
    yield SemesterFactory.get_or_create(name=2)


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
