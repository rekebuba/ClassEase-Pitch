from marshmallow import Schema, ValidationError, pre_load, validates, validates_schema, fields
from api.v1.schemas.user.registration_schema import UserRegistrationSchema
from models.admin import Admin
from api.v1.schemas.base_schema import BaseSchema
from models import storage


class AdminRegistrationSchema(BaseSchema, Schema):
    """Admin schema for validating and serializing Admin data."""
    user_id = fields.UUID(required=False)
    first_name = fields.String(required=True, validate=[
        fields.validate.Length(min=2, max=25)])
    father_name = fields.String(required=True, validate=[
        fields.validate.Length(min=2, max=25)])
    grand_father_name = fields.String(required=True, validate=[
        fields.validate.Length(min=2, max=25)])
    date_of_birth = fields.Date(required=True, format='iso')
    email = fields.Email(required=True)
    gender = fields.String(required=True, validate=[
        fields.validate.OneOf(['M', 'F'])])
    phone = fields.String(required=True)
    address = fields.String(required=True)

    @pre_load
    def set_defaults(self, data, **kwargs):
        # add default values
        self.validate_phone(data['phone'])
        if data.get('gender'):
            data['gender'] = data['gender'].upper()

        return data

    @validates_schema
    def validate_data(self, data, **kwargs):
        if storage.session.query(Admin).filter_by(email=data['email']).first():
            raise ValidationError('Email already exists.')

    @validates('phone')
    def validate_teacher_phone(self, value):
        self.validate_phone(value)
