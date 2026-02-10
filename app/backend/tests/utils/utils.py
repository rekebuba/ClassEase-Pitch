from typing import Dict

from fastapi.testclient import TestClient
from pydantic import EmailStr

from project.api.v1.routers.auth.schema import LoginTokenResponse, MessageResponse
from project.api.v1.routers.auth.service import generate_email_verification_token
from project.core.config import settings


def get_auth_header(client: TestClient, login_data: Dict[str, str]) -> Dict[str, str]:
    """
    Authenticate a user and return the authorization header.

    Args:
        client: The Flask test client.
        username: The username of the user to authenticate.
        password: The password of the user to authenticate.

    Returns:
        A dictionary containing the authorization header.
    """
    r = client.post(
        "/api/v1/auth/login",
        data=login_data,
    )
    assert r.status_code == 200, "Authentication failed"

    result = LoginTokenResponse.model_validate_json(r.text)
    assert result.access_token is not None
    assert result.token_type == "bearer"

    headers = {"Authorization": f"Bearer {result.access_token}"}
    return headers


def moc_verify_email(client: TestClient, email: EmailStr) -> None:
    token = generate_email_verification_token(email)

    r = client.get(f"{settings.API_V1_STR}/auth/verify-email", params={"token": token})

    assert r.status_code == 200

    result = MessageResponse.model_validate_json(r.text)
    assert result.message == "Email successfully verified"
