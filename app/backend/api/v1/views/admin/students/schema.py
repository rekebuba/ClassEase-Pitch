from typing import Any, Dict
from marshmallow import ValidationError, post_dump
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
    post_load,
    pre_load,
    validates_schema,
    fields,
)

from api.v1.utils.typing import PostLoadParam
from api.v1.schemas.schemas import StudentSchema, UserSchema
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
    def set_defaults(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
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

        if data["table_id"] != "":
            data["table"] = self.get_table(data["table_id"])

        return data


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
    def set_defaults(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
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

        if data["table_id"] != "":
            data["table"] = self.get_table(data["table_id"])
            data["value"] = self.update_list_value(
                value, data["table"], data["column_name"]
            )

        return data


class ParamSchema(BaseSchema):
    """Schema for validating parameters."""

    filter_flag = fields.String(required=False)

    filters = fields.List(
        fields.Nested(FilterSchema), required=False, load_default=None, allow_none=True
    )
    valid_filters = fields.List(fields.Raw(), required=False)
    custom_filters = fields.List(fields.Raw(), required=False)
    join_operator = JoinOperatorField(required=False)

    page = fields.Integer(required=False, load_default=1)
    per_page = fields.Integer(required=False, load_default=10)

    sort = fields.List(fields.Nested(SortSchema), required=False)
    valid_sorts = fields.List(fields.Raw(), required=False)
    custom_sorts = fields.List(fields.Raw(), required=False)

    @post_load
    def set_defaults(self, data: PostLoadParam, **kwargs: Any) -> Dict[str, Any]:
        # add default values to the data
        valid_filters = []
        valid_sorts = []
        custom_sorts = []
        custom_filters = []
        for f_item in data["filters"] if data.get("filters") else []:
            if "table" in f_item and f_item["table"] is not None:
                filter = self.filter_data(
                    f_item["table"],
                    f_item["column_name"],
                    f_item["operator"],
                    f_item["value"],
                    f_item["range"],
                )
                valid_filters.extend(filter)
            else:
                custom_filters.append(f_item)
        data.pop("filters", None)
        data["valid_filters"] = valid_filters

        for s_item in data["sort"] if data.get("sort") else []:
            if "table" in s_item and s_item["table"] is not None:
                sort = self.sort_data(
                    s_item["table"], s_item["column_name"], s_item["desc"]
                )
                # Adds all items from result to valid_sorts
                valid_sorts.extend(sort)
            else:
                custom_sorts.append(s_item)

        data.pop("sort", None)
        data["valid_sorts"] = valid_sorts
        data["custom_filters"] = custom_filters
        data["custom_sorts"] = custom_sorts

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
        data["table_id"] = self.get_table_id(STUDYearRecord)

        return data


class GradeSchema(BaseSchema):
    """Schema for validating grade data."""

    id = fields.String(load_only=True)
    grade = fields.Integer(validate=[fields.validate.Range(min=1, max=12)])

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
    grade = fields.Nested(GradeSchema(only=("grade",)), required=True)

    sectionI = fields.String(required=False, allow_none=True)
    sectionII = fields.String(required=False, allow_none=True)

    averageI = fields.String(required=False, allow_none=True)
    averageII = fields.String(required=False, allow_none=True)

    rankI = fields.String(required=False, allow_none=True)
    rankII = fields.String(required=False, allow_none=True)

    year_record = fields.Nested(STUDYearRecordSchema(only=("final_score", "rank")))

    @post_dump
    def merge_nested(self, data: list, many: bool, **kwargs: Any):
        merged_data = {}

        merged_data["tableId"] = self._extract_table_id(data[0] if many else None)
        merged_data["data"] = (
            [self._merge(d) for d in data] if many else [self._merge(data)]
        )

        return merged_data

    def _extract_table_id(self, item):
        table_id = {}
        if not item:
            return table_id

        for model in item.keys():
            entries = item[model]
            if not isinstance(entries, list):
                entries = [entries]

            for entry in entries:
                if isinstance(entry, dict):
                    user_table_id = entry.pop("tableId", None)
                    for key in entry:
                        if isinstance(entry[key], dict):
                            table_id[key] = [(k, user_table_id) for k in entry[key]]
                        else:
                            table_id.setdefault(key, user_table_id)

        return table_id

    def _merge(self, item):
        names = item["student"].pop("studentName")
        full_name = (
            f"{names['firstName']} {names['fatherName']} {names['grandFatherName']}"
        )
        item["student"]["studentName"] = full_name  # Add as a flat field
        result = {
            **item.pop("user", {}),
            **item.pop("student", {}),
            **item.pop("grade", {}),
            **item.pop("yearRecord", {}),
            **item,
        }
        result.pop("tableId", None)
        return result
