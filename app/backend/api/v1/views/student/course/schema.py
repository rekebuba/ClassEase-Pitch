from api.v1.schemas.base_schema import BaseSchema
from marshmallow import fields, pre_dump, pre_load
from typing import Dict, Any


class SubjectSchema(BaseSchema):
    name = fields.String(required=False)
    code = fields.String(required=False)
    subject_id = fields.String(required=True, load_only=True)

    grade = fields.Integer(required=False)
    grade_id = fields.String(required=True, load_only=True)

    @pre_load
    def set_defaults(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        # add default values to the data
        data["grade_id"] = self.get_grade_id(data.pop("grade"))
        data["subject_id"] = self.get_subject_id(
            data.pop("name"), data.pop("code"), data.get("grade_id")
        )

        return data

    @pre_dump
    def add_fields(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        data["grade"] = self.get_grade_detail(id=data.get("grade_id")).grade

        return data


class CourseListSchema(BaseSchema):
    """Schema for validating a list of Course objects."""

    courses = fields.List(fields.Nested(SubjectSchema), required=True)
    student_id = fields.String(required=True, load_only=True)

    academic_year = fields.Integer(required=True)
    semester = fields.Integer(required=True)
    semester_id = fields.String(required=True, load_only=True)

    grade = fields.Integer(required=True)
    grade_id = fields.String(required=False, load_only=True)

    year_id = fields.String(required=False, load_only=True)

    section_id = fields.String(required=False, load_only=True)

    is_registered = fields.Boolean(required=False, load_only=True)

    @pre_load
    def set_defaults(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        # add default values to the data
        data["is_registered"] = self.is_student_registered(data.get("student_id"))
        data["grade_id"] = self.get_grade_id(data.get("grade"))
        data["semester_id"] = self.get_semester_id(
            data.get("semester"), data.get("academic_year")
        )
        data["year_id"] = self.get_year_id(data.get("academic_year"))

        return data
