from datetime import datetime, timedelta
from typing import Any, Dict
import uuid
import bcrypt
from flask import current_app
import jwt

from extension.enums.enum import RoleEnum


def check_password(stored_password: str, provided_password: str) -> bool:
    """Check if the provided password matches the stored hashed password."""
    return bcrypt.checkpw(
        provided_password.encode("utf-8"), stored_password.encode("utf-8")
    )


def create_token(user_id: str, role: RoleEnum) -> str:
    """
    Generate a JWT token for a user based on their role.

    Returns:
        str: A JWT token encoded with the user's ID, expiration time, role, and a unique JTI.

    The token expires in 720 minutes (12 hours) from the time of creation.
    """
    # Determine the secret key based on the role
    secret_keys: Dict[RoleEnum, Any] = {
        RoleEnum.ADMIN: current_app.config["ADMIN_SECRET_KEY"],
        RoleEnum.TEACHER: current_app.config["TEACHER_SECRET_KEY"],
        RoleEnum.STUDENT: current_app.config["STUDENT_SECRET_KEY"],
    }
    secret_key = secret_keys.get(role)
    if not secret_key:
        raise ValueError(f"Invalid role: {role}")

    # Create the payload
    payload = {
        "id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=720),  # 12 hours expiration
        "role": role.value,
        "jti": str(uuid.uuid4()),  # Unique token identifier
    }

    # Encode and return the token
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token
