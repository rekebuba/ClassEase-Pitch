from collections import defaultdict
from typing import Any, Dict, List
from api.v1.schemas.base_schema import BaseSchema
from marshmallow import ValidationError, fields, post_dump

from api.v1.views.admin.students.section_count.type import SectionCountType


class SectionCountsSchema(BaseSchema):
    """Schema for validating student section counts data."""

    section_semester_one = fields.Dict(
        keys=fields.Str(), values=fields.Int(), required=True
    )
    section_semester_two = fields.Dict(
        keys=fields.Str(), values=fields.Int(), required=True
    )
