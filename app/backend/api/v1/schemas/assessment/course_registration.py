from marshmallow import ValidationError, validates_schema, fields, post_load, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from api.v1.schemas.base_schema import BaseSchema
from models import storage

class CourseRegistration(BaseSchema):
    """
    student_id = fields.String(required=True, load_only=True)
    student_yearly_records_id = fields.SubSchema()
    
    grade_id = fields.String(required=True, load_only=True)
    section_id 
    subject_id
    semester_id
    """
    pass
