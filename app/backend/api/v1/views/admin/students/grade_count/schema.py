from api.v1.schemas.base_schema import BaseSchema
from marshmallow import fields


class StudentGradeCountsSchema(BaseSchema):
    """Schema for validating and merging student grade count data."""

    data = fields.Dict(
        keys=fields.Str(),  # Keys must be strings
        values=fields.Int(),  # Values must be integers
        required=True,
    )
