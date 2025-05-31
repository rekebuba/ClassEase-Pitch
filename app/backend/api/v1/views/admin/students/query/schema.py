from typing import Any, Dict, List
from marshmallow import ValidationError, post_dump
from sqlalchemy import ColumnElement, and_
from api.v1.schemas.base_schema import BaseSchema
from api.v1.schemas.config_schema import OPERATOR_CONFIG
from api.v1.schemas.custom_schema import (
    ColumnField,
    FloatOrDateField,
    JoinOperatorField,
    TableField,
    TableIdField,
    ValueField,
)
from marshmallow import (
    validate,
    post_load,
    pre_load,
    validates_schema,
    fields,
)

from api.v1.utils.typing import (
    FilterDict,
    PostFilterDict,
    PostLoadParam,
    PostSortDict,
    SortDict,
)
from api.v1.views.shared.registration.schema import StudentSchema, UserSchema
from models.grade import Grade
from models.stud_year_record import STUDYearRecord


class RangeSchema(BaseSchema):
    """Schema for validating range parameters."""

    min = FloatOrDateField(required=False, allow_none=True)
    max = FloatOrDateField(required=False, allow_none=True)


class SortSchema(BaseSchema):
    """Schema for validating sorting parameters."""

    column_name = ColumnField(required=False)
    desc = fields.Boolean(required=False)
    table_id = TableIdField(required=False)
    table = TableField(required=False)

    @pre_load
    def pre_load_data(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        # add default values to the data
        data["column_name"] = data.pop("id", None)
        table_id = data.get("table_id", None)
        if isinstance(table_id, list):
            if not table_id:
                raise ValidationError("table id list cannot be empty")

            first_table_value = table_id[0][1]  # value (uuid)
            if all(v == first_table_value for _, v in table_id):
                data["column_name"] = [k for k, _ in table_id]
                data["table_id"] = first_table_value  # overwrite with string
            else:
                raise ValidationError(
                    "All values in table id must be the same to extract keys."
                )

        if data.get("table_id", None) is not None and data["table_id"] != "":
            data["table"] = self.get_table(data["table_id"])

        return data

    @post_load
    def post_load_data(self, data: SortDict, **kwargs: Any) -> PostSortDict:
        # add default values to the data
        sorts: PostSortDict = {
            "valid_sorts": [],
            "custom_sorts": data,
        }

        if "table" in data and data["table"] is not None:
            sort = self.sort_data(data["table"], data["column_name"], data["desc"])
            sorts["valid_sorts"].extend(sort)

        return sorts


class FilterSchema(BaseSchema):
    """Schema for validating filter parameters."""

    column_name = ColumnField(required=False, load_default=None, allow_none=True)
    filter_id = fields.String(required=False, load_default=None, allow_none=True)
    table_id = TableIdField(required=False, load_default=None, allow_none=True)
    table = TableField(required=False, load_default=None, allow_none=True)
    range = fields.Nested(
        RangeSchema, required=False, load_default=None, allow_none=True
    )
    variant = fields.String(
        validate=lambda x: x
        in ["text", "number", "multiSelect", "boolean", "date", "dateRange", "range"],
        required=True,
    )
    operator = fields.String(required=False, load_default=None, allow_none=True)
    value = ValueField(required=False, load_default=None, allow_none=True)

    @validates_schema
    def validate_value(self, data: Dict[str, Any], **kwargs: Any) -> None:
        variant = data.get("variant", None)
        operator = data.get("operator", None)

        if not variant:
            raise ValidationError("Missing variant", field_name="variant")

        if operator is not None:
            allowed_operators = OPERATOR_CONFIG.get(variant)
            if not allowed_operators:
                raise ValidationError(
                    f"'{variant}' is not a valid variant.", field_name="variant"
                )

            if operator not in allowed_operators:
                raise ValidationError(
                    f"'{operator}' is not valid for variant '{variant}'",
                    field_name="operator",
                )

    @pre_load
    def pre_load_data(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        # add default values to the data
        data["column_name"] = data.pop("id", None)
        value = data.get("value", None)
        table_id = data.get("table_id", None)
        if isinstance(table_id, list):
            if not table_id:
                raise ValidationError("table id list cannot be empty")

            first_table_value = table_id[0][1]  # value (uuid)
            if all(v == first_table_value for _, v in table_id):
                data["column_name"] = [k for k, _ in table_id]
                data["table_id"] = first_table_value  # overwrite with string
            else:
                raise ValidationError(
                    "All values in table id must be the same to extract keys."
                )

        if data.get("table_id", None) is not None and data["table_id"] != "":
            """If table_id is provided, fetch the table."""
            data["table"] = self.get_table(data["table_id"])
            data["value"] = self.update_list_value(
                value, data["table"], data["column_name"]
            )

        return data

    @post_load
    def post_load_data(self, data: FilterDict, **kwargs: Any) -> PostFilterDict:
        filters: PostFilterDict = {
            "valid_filters": [],
            "custom_filters": data,
        }
        if "table" in data and data["table"] is not None:
            filter = self.filter_data(
                data["table"],
                data["column_name"],
                data["operator"],
                data["value"],
                data["range"],
            )
            filters["valid_filters"].extend(filter)

        return filters


class ParamSchema(BaseSchema):
    """Schema for validating parameters."""

    filter_flag = fields.String(required=False)

    filters = fields.List(
        fields.Nested(FilterSchema), required=False, load_default=[], allow_none=True
    )
    sorts = fields.List(fields.Nested(SortSchema), required=False, load_default=[])
    join_operator = JoinOperatorField(required=False, load_default=and_)

    page = fields.Integer(required=False, load_default=1)
    per_page = fields.Integer(required=False, load_default=10)


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
        data["table_id"] = self.get_table_id(STUDYearRecord)

        return data


class GradeSchema(BaseSchema):
    """Schema for validating grade data."""

    id = fields.String(load_only=True)
    grade = fields.Integer(
        validate=[validate.Range(min=1, max=12)],
        required=False,
        allow_none=True,
        dump_default=None,
    )

    table_id = fields.String(required=False)

    @post_dump
    def add_fields(self, data, **kwargs: Any):
        data["table_id"] = self.get_table_id(Grade)

        return data


class AllStudentsSchema(BaseSchema):
    user = fields.Nested(
        UserSchema(only=("identification", "image_path", "created_at"))
    )
    # it will be returned as a string ex: "John Doe Smith"
    student = fields.Nested(
        StudentSchema(
            only=("student_name", "guardian_name", "guardian_phone", "is_active")
        )
    )
    grade = fields.Nested(
        GradeSchema(only=("grade",)), required=False, allow_none=False
    )

    sectionI = fields.String(required=False, allow_none=True)
    sectionII = fields.String(required=False, allow_none=True)

    averageI = fields.Float(required=False, allow_none=True)
    averageII = fields.Float(required=False, allow_none=True)

    rankI = fields.Integer(required=False, allow_none=True)
    rankII = fields.Integer(required=False, allow_none=True)

    year_record = fields.Nested(
        STUDYearRecordSchema(only=("final_score", "rank")),
        required=False,
        allow_none=False,
    )
