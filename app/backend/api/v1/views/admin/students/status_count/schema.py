from api.v1.schemas.base_schema import BaseSchema
from marshmallow import fields


class StudentStatusSchema(BaseSchema):
    """Schema for validating student status data."""

    active = fields.Integer(required=True, dump_default=0)
    inactive = fields.Integer(required=True, dump_default=0)
    suspended = fields.Integer(required=True, dump_default=0)
    graduated = fields.Integer(required=False)
    graduated_with_honors = fields.Integer(required=False)
