from typing import Any, Dict, List
from api.v1.schemas.base_schema import BaseSchema
from marshmallow import fields, post_dump

from api.v1.views.admin.students.grade_count.type import GradeCountType


class StudentGradeCountsSchema(BaseSchema):
    """Schema for validating and merging student grade or section count data."""

    grade = fields.String(required=False, load_default=None)
    total = fields.Integer(required=False, load_default=0, dump_default=0)

    @post_dump
    def merge_nested(
        self, data: List[GradeCountType], many: bool, **kwargs: Any
    ) -> Dict[str, int]:
        if many:
            # Default for grade keys 1–12
            result: Dict[str, int] = {str(i): 0 for i in range(1, 13)}

            for item in data:
                result[item["grade"]] = item["total"]

            return result
        return {}
