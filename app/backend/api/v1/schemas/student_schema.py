from datetime import datetime
from marshmallow import ValidationError, pre_load, validates, validates_schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.user import User
from models.student import Student
from api.v1.schemas.user_schema import UserSchema
from api.v1.schemas.base_schema import BaseSchema
from models import storage
from pyethiodate import EthDate


class StudentSchema(BaseSchema, SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        sqla_session = storage.session
        load_instance = True
        include_relationships = True
        exclude = ('id',)

    user_id = fields.UUID(required=False)
    name = fields.String(required=True, validate=[
                         fields.validate.Length(min=2, max=25)])
    father_name = fields.String(required=True, validate=[
                                fields.validate.Length(min=2, max=25)])
    grand_father_name = fields.String(required=True, validate=[
                                      fields.validate.Length(min=2, max=25)])

    date_of_birth = fields.DateTime(required=True)
    father_phone = fields.String(required=False)
    mother_phone = fields.String(required=False)

    @validates_schema
    def validate_phones(self, data, **kwargs):
        if not data.get('father_phone') and not data.get('mother_phone'):
            raise ValidationError('Either father_phone or mother_phone must be provided.')

    @pre_load
    def set_default_years(self, data, **kwargs):
        current_EC_year = EthDate.date_to_ethiopian(datetime.now()).year
        current_GC_year = f'{current_EC_year + 7}/ {current_EC_year + 8}'
        data.setdefault('start_year_EC', current_EC_year)
        data.setdefault('start_year_GC', current_GC_year)
        return data

    start_year_EC = fields.String(required=False)
    start_year_GC = fields.String(required=False)

    end_year = fields.String(required=False)

    previous_school = fields.String(required=False)

    current_grade = fields.Integer(required=True)
    semester_id = fields.UUID(required=False)
    has_passed = fields.Boolean(required=False)
    registration_window_start = fields.DateTime(required=False)
