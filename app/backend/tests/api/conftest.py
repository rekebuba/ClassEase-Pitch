import uuid
from collections.abc import Generator
from typing import Dict

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from project.api.v1.routers.dependencies import get_db
from project.api.v1.routers.registrations.schema import RegistrationResponse
from project.core.config import settings
from project.core.db import engine, init_db
from project.main import app
from project.models import Parent
from project.models.base.base_model import Base
from project.models.year import Year
from tests.factories.api_data import NewYearFactory, ParentRegistrationFactory
from tests.utils.utils import get_auth_header

# Session factory
TestingSessionLocal = sessionmaker(bind=engine, autoflush=True, expire_on_commit=False)


# Override the get_db dependency to use test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Apply the override
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    Base.metadata.create_all(bind=engine)

    with TestingSessionLocal() as session:
        init_db(session)

    yield

    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="module")
def db_session() -> Generator[Session, None, None]:
    """Provide a database session for each test with rollback"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()  # Rollback any changes
        connection.close()  # Close connection


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestingSessionLocal() as session:
        session.rollback()  # Ensure clean state for each test

    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def admin_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD.get_secret_value(),
    }
    return get_auth_header(client, login_data)


@pytest.fixture(scope="module")
def teacher_token_headers(client: TestClient) -> dict[str, str]:
    return get_auth_header(client, {})


@pytest.fixture(scope="module")
def student_token_headers(client: TestClient) -> dict[str, str]:
    return get_auth_header(client, {})


@pytest.fixture(scope="module")
def existing_year(
    db_session: Session,
) -> Year | None:
    year = db_session.execute(select(Year)).scalars().first()
    return year


@pytest.fixture(scope="module")
def year(
    client: TestClient,
    db_session: Session,
    admin_token_headers: Dict[str, str],
    existing_year: Year | None,
) -> Year:
    if existing_year:
        return existing_year

    data = NewYearFactory.create(setup_methods="Default Template")

    r = client.post(
        f"{settings.API_V1_STR}/years",
        json=data.model_dump(mode="json", by_alias=True),
        headers=admin_token_headers,
    )
    assert r.status_code == 201
    assert r.json() is not None

    result = r.json()

    assert "id" in result
    assert "message" in result
    assert "Year created Successfully" == result["message"]

    try:
        year_id = uuid.UUID(result["id"])
    except ValueError:
        assert False, "Year ID is not a valid UUID"

    year = db_session.scalar(
        select(Year)
        .join(Year.grades)
        .join(Year.subjects)
        .where(Year.id == year_id)
        .distinct()
    )
    assert year is not None

    return year


@pytest.fixture(scope="module")
def parent(
    client: TestClient,
    db_session: Session,
    admin_token_headers: Dict[str, str],
) -> Parent:
    """Fixture to create a parent for testing"""

    parent = ParentRegistrationFactory.build()

    r = client.post(
        f"{settings.API_V1_STR}/register/parents",
        json=parent.model_dump(mode="json", by_alias=True),
        headers=admin_token_headers,
    )

    assert r.status_code == 201

    result = RegistrationResponse.model_validate_json(r.text)

    assert "Parent Registered Successfully" == result.message

    parent = db_session.get(Parent, result.id)

    assert parent is not None

    return parent
