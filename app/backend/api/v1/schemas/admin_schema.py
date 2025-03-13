from marshmallow import Schema, ValidationError, pre_load, validates, validates_schema, fields
from api.v1.schemas.user_schema import UserRegistrationSchema
from models.admin import Admin
from api.v1.schemas.base_schema import BaseSchema
from models import storage


class AdminRegistrationSchema(BaseSchema):
    """Admin schema for validating and serializing Admin data."""
    user_id = fields.String(required=False)
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


class SubjectSchema(BaseSchema):
    subject = fields.String(required=True)
    subject_code = fields.String(required=True, load_only=True)
    subject_id = fields.String(required=True, load_only=True)

    @pre_load
    def set_defaults(self, data, **kwargs):
        # add default values to the data
        data['subject_id'] = self.get_subject_id(
            data.get('subject'), data.get('subject_code'), data.get('grade_id'))

        return data


class MarkListTypeSchema(BaseSchema):
    type = fields.String(required=True, load_only=True)
    percentage = fields.Integer(required=True, load_only=True)


class CreateMarkListSchema(BaseSchema):
    grade = fields.Integer(required=True, load_only=True)
    grade_id = fields.String(required=False, load_only=True)

    subjects = fields.List(fields.Nested(SubjectSchema), required=True)

    academic_year = fields.Integer(required=True, load_only=True)
    semester = fields.Integer(required=True, load_only=True)
    semester_id = fields.String(required=True, load_only=True)

    assessment_type = fields.List(
        fields.Nested(MarkListTypeSchema), required=True)

    @pre_load
    def set_defaults(self, data, **kwargs):
        # add default values to the data
        data['grade_id'] = self.get_grade_id(data.get('grade'))
        data['semester_id'] = self.get_semester_id(
            data.get('semester'), data.get('academic_year'))

        return data
