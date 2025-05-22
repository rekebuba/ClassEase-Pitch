from api.v1.schemas.base_schema import BaseSchema
from marshmallow import fields

from api.v1.schemas.schemas import RangeSchema


class StudentAverageSchema(BaseSchema):
    """Schema for validating student average data."""

    total_average = fields.Nested(RangeSchema, required=True)
    averageI = fields.Nested(RangeSchema, required=True)
    averageII = fields.Nested(RangeSchema, required=True)
    rank = fields.Nested(RangeSchema, required=True)
    rankI = fields.Nested(RangeSchema, required=True)
    rankII = fields.Nested(RangeSchema, required=True)
