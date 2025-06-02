from api.v1.schemas.base_schema import BaseSchema
from marshmallow import fields

from api.v1.schemas.schemas import RangeSchema


class StudentAverageSchema(BaseSchema):
    """Schema for validating student average data."""

    total_average = fields.Nested(RangeSchema, required=True)
    average_semester_one = fields.Nested(RangeSchema, required=True)
    average_semester_two = fields.Nested(RangeSchema, required=True)
    rank = fields.Nested(RangeSchema, required=True)
    rank_semester_one = fields.Nested(RangeSchema, required=True)
    rank_semester_two = fields.Nested(RangeSchema, required=True)
