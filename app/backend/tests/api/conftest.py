import random
from collections.abc import Generator
from typing import Dict

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from api.v1.routers.dependencies import get_db
from core.config import settings
from core.db import init_db, test_engine
from main import app
from models.base.base_model import Base
from models.year import Year
from tests.utils.utils import get_auth_header, get_year

# Session factory
TestingSessionLocal = sessionmaker(
    bind=test_engine, autoflush=False, autocommit=False, expire_on_commit=False
)


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
    Base.metadata.create_all(bind=test_engine)

    with TestingSessionLocal() as session:
        init_db(session)

    yield

    # Base.metadata.drop_all(bind=test_engine)
    # test_engine.dispose()


@pytest.fixture(scope="module")
def db_session() -> Generator[Session, None, None]:
    """Provide a database session for each test with rollback"""
    connection = test_engine.connect()
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
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    return get_auth_header(client, login_data)


@pytest.fixture(scope="module")
def teacher_token_headers(client: TestClient) -> dict[str, str]:
    return get_auth_header(client, {})


@pytest.fixture(scope="module")
def student_token_headers(client: TestClient) -> dict[str, str]:
    return get_auth_header(client, {})


@pytest.fixture(scope="module")
def year(
    db_session: Session, client: TestClient, admin_token_headers: Dict[str, str]
) -> Year:
    years = db_session.scalars(select(Year)).all()

    if len(years) > 0:
        return random.choice(years)

    return get_year(client, admin_token_headers, db_session)
