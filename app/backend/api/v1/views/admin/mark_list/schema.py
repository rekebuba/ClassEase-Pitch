from typing import Any, Dict
from api.v1.schemas.base_schema import BaseSchema
from marshmallow import fields, pre_load

from api.v1.schemas.schemas import SubjectSchema


class MarkListTypeSchema(BaseSchema):
    type = fields.String(required=True)
    percentage = fields.Integer(required=True)


class MarkAssessmentSchema(BaseSchema):
    grade = fields.Integer(required=False)
    grade_id = fields.String(required=True)

    semester_id = fields.String(required=True, load_only=True)
    section_id = fields.String(required=False, load_only=True, allow_none=True)

    subjects = fields.List(fields.Nested(SubjectSchema), required=True)

    assessment_type = fields.List(fields.Nested(MarkListTypeSchema), required=True)

    @pre_load
    def set_defaults(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        # add default values to the data
        data["grade_id"] = self.get_grade_id(data.pop("grade"))
        return data


class CreateMarkListSchema(BaseSchema):
    mark_assessment = fields.List(fields.Nested(MarkAssessmentSchema), required=True)

    academic_year = fields.Integer(required=False, load_only=True)
    semester = fields.Integer(required=False, load_only=True)
    semester_id = fields.String(required=True, load_only=True)

    @pre_load
    def set_defaults(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        # add default values to the data
        data["semester_id"] = self.get_semester_id(
            data.pop("semester"), data.pop("academic_year")
        )

        # Pass semester_id to each item in mark_assessment
        for item in data.get("mark_assessment", []):
            item["semester_id"] = data["semester_id"]

        return data
