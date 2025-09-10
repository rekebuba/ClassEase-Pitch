import uuid
from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from core.config import settings
from models.year import Year
from tests.factories.api_data import NewYearFactory


def get_auth_header(client: TestClient, login_data: Dict[str, str]) -> Dict[str, str]:
    """
    Authenticate a user and return the authorization header.

    Args:
        client: The Flask test client.
        identification: The identification of the user to authenticate.
        password: The password of the user to authenticate.

    Returns:
        A dictionary containing the authorization header.
    """
    response = client.post(
        "/api/v1/auth/login",
        data=login_data,
    )
    assert response.status_code == 200, "Authentication failed"
    assert response.json is not None

    tokens = response.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


def get_year(
    client: TestClient, admin_token_headers: Dict[str, str], db_session: Session
) -> Year:
    data = NewYearFactory.create()
    data.setup_methods = "Default Template"

    r = client.post(
        f"{settings.API_V1_STR}/years",
        json=data.model_dump(mode="json", by_alias=True),
        headers=admin_token_headers,
    )
    assert r.status_code == 201
    assert r.json() is not None

    result = r.json()

    year = db_session.get(Year, result["id"])
    assert year is not None

    return year
