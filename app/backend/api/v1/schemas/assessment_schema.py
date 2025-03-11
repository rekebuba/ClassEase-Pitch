from marshmallow import ValidationError, pre_load, validates_schema, fields, post_load, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from api.v1.schemas.base_schema import BaseSchema
from models import storage


class CourseRegistrationSchema(BaseSchema):
    grade = fields.Integer(required=True, load_only=True)
    grade_id = fields.String(required=False, load_only=True)

    subject = fields.String(required=True, load_only=True)
    subject_code = fields.String(required=True, load_only=True)
    subject_id = fields.String(required=True, load_only=True)

    @pre_load
    def set_defaults(self, data, **kwargs):
        # add default values to the data
        data['grade_id'] = self.get_grade_id(data.get('grade'))
        data['subject_id'] = self.get_subject_id(
            data.get('subject'), data.get('subject_code'), data.get('grade_id'))

        return data


class CourseListSchema(BaseSchema):
    """Schema for validating a list of Course objects."""
    course = fields.List(fields.Nested(
        CourseRegistrationSchema), required=True)
    student_id = fields.String(required=True, load_only=True)
    user_id = fields.String(required=True, load_only=True)

    academic_year = fields.Integer(required=True, load_only=True)
    semester = fields.Integer(required=True, load_only=True)
    semester_id = fields.String(required=True, load_only=True)

    grade = fields.Integer(required=True, load_only=True)
    grade_id = fields.String(required=False, load_only=True)

    year_record_id = fields.String(required=False, load_only=True)

    section_id = fields.String(required=False, load_only=True)

    @pre_load
    def set_defaults(self, data, **kwargs):
        data['user_id'] = self.get_user_id(data.get('student_id'))
        data['grade_id'] = self.get_grade_id(data.get('grade'))
        data['semester_id'] = self.get_semester_id(
            data.get('semester'), data.get('academic_year'))

        return data
