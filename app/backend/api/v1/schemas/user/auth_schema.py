import bcrypt
from marshmallow import ValidationError, validates_schema, fields, post_load, Schema 
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from api.v1.schemas.base_schema import BaseSchema
from models.user import User
from werkzeug.datastructures import FileStorage
from models import storage


class AuthSchema(BaseSchema, Schema):
    """Schema for validating user authentication data."""
    identification = fields.String(required=True, load_only=True)
    password = fields.String(required=True, load_only=True)
    role = fields.String(required=False)

    @staticmethod
    def _check_password(stored_password, provided_password):
        """Check if the provided password matches the stored hashed password."""
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

    @validates_schema
    def validate_data(self, data, **kwargs):
        user = storage.session.query(User).filter_by(identification=data['identification']).first()
        if user is None or not AuthSchema._check_password(user.password, data['password']):
            raise ValidationError('Invalid credentials.')

    @post_load
    def load_user(self, data, **kwargs):
        return storage.session.query(User).filter_by(identification=data['identification']).first().to_dict()
