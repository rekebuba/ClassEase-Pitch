from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    """Schema for validating user authentication data."""

    identification: str
    password: str


class LogOutResponse(BaseModel):
    message: str
