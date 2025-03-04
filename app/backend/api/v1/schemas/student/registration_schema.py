import re
from pyethiodate import EthDate
from datetime import datetime
from marshmallow import Schema, ValidationError, post_load, pre_load, validates, validates_schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.user import User
from models.student import Student
from api.v1.schemas.user.registration_schema import UserRegistrationSchema
from api.v1.schemas.base_schema import BaseSchema
from models import storage
import tests.test_api.helper_functions


def current_EC_year() -> str:
    return str(EthDate.date_to_ethiopian(datetime.now()).year)


def current_GC_year():
    return f'{int(current_EC_year()) + 7}/{int(current_EC_year()) + 8}'


class StudentRegistrationSchema(BaseSchema, Schema):
    """Student schema for validating and serializing Student data."""
    user_id = fields.String(required=False)
    first_name = fields.String(required=True, validate=[
        fields.validate.Length(min=2, max=25)])
    father_name = fields.String(required=True, validate=[
                                fields.validate.Length(min=2, max=25)])
    grand_father_name = fields.String(required=True, validate=[
                                      fields.validate.Length(min=2, max=25)])
    guardian_name = fields.String(required=False, validate=[
                                  fields.validate.Length(min=2, max=25)])
    date_of_birth = fields.Date(required=True, format='iso')
    gender = fields.String(required=True, validate=[
                           fields.validate.OneOf(['M', 'F'])])

    father_phone = fields.String(required=False)
    mother_phone = fields.String(required=False)
    guardian_phone = fields.String(required=False)

    start_year_ethiopian = fields.String(required=False)
    start_year_gregorian = fields.String(required=False)
    end_year_ethiopian = fields.String(required=False)
    end_year_gregorian = fields.String(required=False)

    previous_school = fields.String(required=False, validate=[
                                    fields.validate.Length(min=2, max=12)])

    current_grade = fields.Integer(required=True, validate=[
                                   fields.validate.Range(min=1, max=12)])
    semester_id = fields.UUID(required=False)
    has_passed = fields.Boolean(required=False, dump_default=False)
    registration_window_start = fields.DateTime(required=False)

    birth_certificate = fields.String(required=False)

    has_medical_condition = fields.Boolean(required=False, dump_default=False)
    medical_details = fields.String(required=False)
    has_disability = fields.Boolean(required=False, dump_default=False)
    disability_details = fields.String(required=False)
    requires_special_accommodation = fields.Boolean(
        required=False, dump_default=False)
    special_accommodation_details = fields.String(required=False)

    is_transferring = fields.Boolean(required=False, dump_default=False)
    is_active = fields.Boolean(required=False, dump_default=True)

    @pre_load
    def set_defaults(self, data, **kwargs):
        # add default values for start_year_ethiopian and start_year_gregorian
        if not data.get('start_year_ethiopian'):
            data['start_year_ethiopian'] = current_EC_year()
        if not data.get('start_year_gregorian'):
            data['start_year_gregorian'] = current_GC_year()
        if data.get('gender'):
            data['gender'] = data['gender'].upper()

        return data

    @validates_schema
    def validate_data(self, data, **kwargs):
        if not data.get('father_phone') and not data.get('mother_phone'):
            raise ValidationError(
                'Either father_phone or mother_phone must be provided.')

    @validates('date_of_birth')
    def validate_date_of_birth(self, value):
        if value > datetime.now().date():
            raise ValidationError('Date of birth cannot be in the future.')

    @validates('father_phone')
    def validate_father_phone(self, value):
        self.validate_phone(value)

    @validates('mother_phone')
    def validate_mother_phone(self, value):
        self.validate_phone(value)

    @validates('guardian_phone')
    def validate_guardian_phone(self, value):
        if value:  # Optional field, only validate if provided
            self.validate_phone(value)
