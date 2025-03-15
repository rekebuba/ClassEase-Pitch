import re
from datetime import datetime
from marshmallow import Schema, ValidationError, post_load, pre_load, validates, validates_schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.year import Year
from models.semester import Semester
from models.user import User
from models.student import Student
from api.v1.schemas.user_schema import UserRegistrationSchema
from api.v1.schemas.year_schema import YearIdField
from api.v1.schemas.base_schema import BaseSchema
from models import storage
import tests.test_api.helper_functions


class StudentRegistrationSchema(BaseSchema):
    """Student schema for validating and serializing Student data."""
    user_id = fields.String(required=False, load_default=None)
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

    academic_year = fields.Integer(required=True, validate=[
        fields.validate.Range(min=2000, max=2100)])
    start_year_id = fields.String(required=False, load_default=None)
    current_year_id = fields.String(required=False, load_default=None)

    is_transfer = fields.Boolean(required=False)
    previous_school_name = fields.String(required=False, validate=[
        fields.validate.Length(min=2, max=50)], allow_none=True)

    current_grade = fields.Integer(required=False, validate=[
                                   fields.validate.Range(min=1, max=12)])
    current_grade_id = fields.String(required=True)

    semester_id = fields.String(required=False)
    has_passed = fields.Boolean(required=False, load_default=False)
    next_grade = fields.Integer(required=False, validate=[
        fields.validate.Range(min=1, max=12)
    ])
    is_registered = fields.Boolean(required=False)

    birth_certificate = fields.String(required=False)

    has_medical_condition = fields.Boolean(required=False)
    medical_details = fields.String(required=False, validate=[
        fields.validate.Length(min=5, max=500)
    ], allow_none=True)
    has_disability = fields.Boolean(required=False)
    disability_details = fields.String(required=False, validate=[
        fields.validate.Length(min=5, max=500)
    ], allow_none=True)
    requires_special_accommodation = fields.Boolean(required=False)
    special_accommodation_details = fields.String(required=False, validate=[
        fields.validate.Length(min=5, max=500)
    ], allow_none=True)

    is_active = fields.Boolean(required=False, load_default=False)

    @pre_load
    def set_defaults(self, data, **kwargs):
        # add default values to the data
        data['current_grade_id'] = self.get_grade_id(data.pop('current_grade'))

        data['start_year_id'] = self.get_year_id(data['academic_year'])
        data['current_year_id'] = self.get_year_id(data['academic_year'])
        data['gender'] = data.get('gender').upper()

        data['is_transfer'] = data.get('is_transfer') == 'True'
        data['has_disability'] = data.get('has_disability') == 'True'
        data['has_medical_condition'] = data.get(
            'has_medical_condition') == 'True'
        data['requires_special_accommodation'] = data.get(
            'requires_special_accommodation') == 'True'

        if not data.get('is_transfer') and not data.get('previous_school_name', '').strip():
            data['previous_school_name'] = None

        if not data.get('has_medical_condition') and not data.get('medical_details', '').strip():
            data['medical_details'] = None

        if not data.get('has_disability') and not data.get('disability_details', '').strip():
            data['disability_details'] = None

        if not data.get('requires_special_accommodation') and not data.get('special_accommodation_details', '').strip():
            data['special_accommodation_details'] = None

        return data

    @validates_schema
    def validate_data(self, data, **kwargs):
        if not data.get('father_phone') and not data.get('mother_phone'):
            raise ValidationError(
                'Either father_phone or mother_phone must be provided.')
        if data.get('is_transfer') and not data.get('previous_school_name'):
            raise ValidationError(
                'previous_school_name must be provided if is_transfer is True.')
        if data.get('is_transfer') == False and data.get('previous_school_name'):
            raise ValidationError(
                'previous_school_name must be None if is_transfer is False.')
        if data.get('has_medical_condition') and not data.get('medical_details'):
            raise ValidationError(
                'medical_details must be provided if has_medical_condition is True.')
        if data.get('has_medical_condition') == False and data.get('medical_details'):
            raise ValidationError(
                'medical_details must be None if has_medical_condition is False.')
        if data.get('has_disability') and not data.get('disability_details'):
            raise ValidationError(
                'disability_details must be provided if has_disability is True.')
        if data.get('has_disability') == False and data.get('disability_details'):
            raise ValidationError(
                'disability_details must be None if has_disability is False.')
        if data.get('requires_special_accommodation') == True and not data.get('special_accommodation_details'):
            raise ValidationError(
                'special_accommodation_details must be provided if requires_special_accommodation is True.')
        if data.get('requires_special_accommodation') == False and data.get('special_accommodation_details'):
            raise ValidationError(
                'special_accommodation_details must be None if requires_special_accommodation is False.')

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

    @validates('semester_id')
    def validate_semester_id(self, value):
        if value:
            semester = storage.get_first(Semester, id=value)
            if not semester:
                raise ValidationError('Invalid semester_id.')
