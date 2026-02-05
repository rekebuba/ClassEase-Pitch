from typing import Dict

from fastapi.testclient import TestClient


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
