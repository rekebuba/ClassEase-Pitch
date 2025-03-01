from marshmallow import ValidationError, validates, validates_schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.user import User
from models.admin import Admin
from api.v1.schemas.user_schema import UserSchema
from api.v1.schemas.base_schema import BaseSchema
from models import storage


class AdminSchema(BaseSchema, SQLAlchemyAutoSchema):
    class Meta:
        model = Admin
        sqla_session = storage.session  # Provide the SQLAlchemy session
        load_instance = True
        include_relationships = True
        exclude = ('id',)

    name = fields.String(required=True, validate=[
                         fields.validate.Length(min=2, max=25)])
    email = fields.Email(required=True)
    user_id = fields.UUID(required=False)

    @validates('email')
    def validate_email(self, value, **kwargs):
        session = self.session

        if session.query(Admin).filter_by(email=value).first():
            raise ValidationError('Email already exists.')
