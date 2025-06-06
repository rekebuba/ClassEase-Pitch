from typing import Any, Dict
import bcrypt
from api.v1.utils.typing import AuthType
from api.v1.schemas.custom_schema import RoleEnumField
from api.v1.schemas.base_schema import BaseSchema
from marshmallow import (
    post_load,
    validates_schema,
    fields,
)
from models import storage
from models.user import User


class InvalidCredentialsError(Exception):
    """Exception raised when invalid credentials are provided."""

    pass


class AuthSchema(BaseSchema):
    """Schema for validating user authentication data."""

    identification = fields.String(required=True, load_only=True, data_key="id")
    password = fields.String(required=True, load_only=True)
    role = RoleEnumField()
    api_key = fields.String()
    message = fields.String(dump_only=True)

    @staticmethod
    def _check_password(stored_password: str, provided_password: str) -> bool:
        """Check if the provided password matches the stored hashed password."""
        return bcrypt.checkpw(
            provided_password.encode("utf-8"), stored_password.encode("utf-8")
        )

    @validates_schema
    def validate_data(self, data: Dict[str, Any], **kwargs: Any) -> None:
        user = (
            storage.session.query(User)
            .filter_by(identification=data["identification"])
            .first()
        )

        if user is None or not AuthSchema._check_password(
            user.password, data["password"]
        ):
            raise InvalidCredentialsError("Invalid credentials.")

    @post_load
    def load_user(self, data: AuthType, **kwargs: Any) -> AuthType:
        user_role = (
            storage.session.query(User.role)
            .filter_by(identification=data["identification"])
            .scalar()
        )
        return {"role": user_role, "identification": data["identification"]}
