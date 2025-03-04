from marshmallow import Schema, ValidationError, fields, validates
from api.v1.schemas.base_schema import BaseSchema


class SemesterCreationSchema(BaseSchema):
    """Schema for validating semester creation data."""
    event_id = fields.String(required=True, load_only=True)
    name = fields.Integer(required=True, load_only=True, validate=[
                          fields.validate.Range(min=1, max=2)])
