from typing import Any, Dict
from marshmallow import (
    post_dump,
    pre_load,
    fields,
    validate,
)
from api.v1.schemas.base_schema import BaseSchema
from api.v1.schemas.custom_schema import (
    FloatOrDateField,
)
from models.section import Section
from models.academic_term import AcademicTerm
from models.student_year_record import StudentYearRecord
from models.grade import Grade


class InvalidCredentialsError(Exception):
    """Exception raised when invalid credentials are provided."""

    pass


class FullNameSchema(BaseSchema):
    """Student name schema for validating and serializing Student data."""

    first_name = fields.String(required=True, validate=[validate.Length(min=2, max=25)])
    father_name = fields.String(
        required=True, validate=[validate.Length(min=2, max=25)]
    )
    grand_father_name = fields.String(
        required=True, validate=[validate.Length(min=2, max=25)]
    )


class GradeSchema(BaseSchema):
    """Schema for validating grade data."""

    grade = fields.Integer(validate=[validate.Range(min=1, max=12)])
    grade = fields.Integer(validate=[validate.Range(min=1, max=12)])

    table_id = fields.String(required=False)

    @post_dump
    def add_fields(self, data, **kwargs: Any):
        data["table_id"] = self.get_table_id(Grade)

        return data


class SubjectSchema(BaseSchema):
    subject = fields.String(required=False)
    subject_code = fields.String(required=False)
    subject_id = fields.String(required=True, load_only=True)

    grade = fields.Integer(required=False)
    grade_id = fields.String(required=True, load_only=True)

    @pre_load
    def set_defaults(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        # add default values to the data
        data["grade_id"] = self.get_grade_id(data.pop("grade"))
        data["subject_id"] = self.get_subject_id(
            data.pop("subject"), data.pop("subject_code"), data.get("grade_id")
        )

        return data


class RangeSchema(BaseSchema):
    """Schema for validating range parameters."""

    min = FloatOrDateField(required=False, allow_none=True)
    max = FloatOrDateField(required=False, allow_none=True)


class SectionSchema(BaseSchema):
    id = fields.String(data_key="section_id")
    semester_id = fields.String(required=False)
    semester = fields.Integer(required=False)
    section = fields.String()

    table_id = fields.String(required=False)

    @post_dump
    def add_fields(self, data, **kwargs: Any):
        """Add table_id to the dumped data."""
        data["table_id"] = self.get_table_id(Section)
        return data


class SemesterSchema(BaseSchema):
    event_id = fields.String(required=False)
    name = fields.Integer(required=False)

    @post_dump
    def add_fields(self, data, **kwargs: Any):
        """Add table_id to the dumped data."""
        data["table_id"] = self.get_table_id(Semester)
        return data


class STUDYearRecordSchema(BaseSchema):
    user_id = fields.String()
    grade_id = fields.String()

    year = fields.String()
    year_id = fields.String()

    final_score = fields.Float(dump_default=0.0)
    rank = fields.Integer(dump_default=0)

    table_id = fields.String(required=False)

    @post_dump
    def add_fields(self, data, **kwargs: Any):
        data["table_id"] = self.get_table_id(StudentYearRecord)

        return data
