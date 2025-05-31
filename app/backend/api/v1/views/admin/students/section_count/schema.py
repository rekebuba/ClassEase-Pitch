from collections import defaultdict
from typing import Any, Dict, List
from api.v1.schemas.base_schema import BaseSchema
from marshmallow import ValidationError, fields, post_dump

from api.v1.views.admin.students.section_count.type import SectionCountType


class TotalSectionSchema(BaseSchema):
    """Schema for validating student section data."""

    section = fields.String(required=False, load_default=None)
    total = fields.Integer(required=False, load_default=0, dump_default=0)


class SectionCountsSchema(BaseSchema):
    """Schema for validating student section counts data."""

    sectionI = fields.Nested(TotalSectionSchema)
    sectionII = fields.Nested(TotalSectionSchema)
