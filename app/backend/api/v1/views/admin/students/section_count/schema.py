from collections import defaultdict
from typing import Any, Dict, List
from api.v1.schemas.base_schema import BaseSchema
from marshmallow import fields, post_dump

from api.v1.views.admin.students.section_count.type import SectionCountType


class TotalSectionSchema(BaseSchema):
    """Schema for validating student section data."""

    section = fields.String(required=False, load_default=None)
    total = fields.Integer(required=False, load_default=0, dump_default=0)


class SectionCountsSchema(BaseSchema):
    """Schema for validating student section counts data."""

    sectionI = fields.Nested(TotalSectionSchema)
    sectionII = fields.Nested(TotalSectionSchema)

    @post_dump
    def merge_nested(
        self, data: List[SectionCountType], many: bool, **kwargs: Any
    ) -> Dict[str, Dict[str, int]]:
        if many:
            result: defaultdict[str, defaultdict[str, int]] = defaultdict(
                lambda: defaultdict(int)
            )

            for item in data:
                for section, values in item.items():
                    # Ensure values is a dict before indexing
                    name = values["section"]
                    total = values["total"]
                    result[section][name] += total

            # Convert defaultdicts to regular dicts
            final_result: Dict[str, Dict[str, int]] = {
                sec: dict(names) for sec, names in result.items()
            }

            return final_result

        return {}
