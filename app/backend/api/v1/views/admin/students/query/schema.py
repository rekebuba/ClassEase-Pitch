from typing import Any, Dict, List, Union
from marshmallow import ValidationError, post_dump
from sqlalchemy import ColumnElement, True_, UnaryExpression, and_, true
from api.v1.schemas.base_schema import BaseSchema
from api.v1.schemas.config_schema import ALISA_NAME, OPERATOR_CONFIG, to_snake_case_key
from api.v1.schemas.custom_schema import (
    ColumnField,
    DecimalEncoder,
    FloatOrDateField,
    JoinOperatorField,
    TableField,
    ValueField,
)
from marshmallow import (
    validate,
    post_load,
    pre_load,
    validates_schema,
    fields,
)

from api.v1.schemas.schemas import SectionSchema, SemesterSchema
from api.v1.utils.typing import (
    FilterDict,
    PostFilterDict,
    PostLoadParam,
    PostSortDict,
    SortDict,
)
from api.v1.views.shared.registration.schema import StudentSchema, UserSchema
from models.grade import Grade
from models.section import Section
from models.semester import Semester
from models.stud_semester_record import STUDSemesterRecord
from models.stud_year_record import STUDYearRecord


class RangeSchema(BaseSchema):
    """Schema for validating range parameters."""

    min = FloatOrDateField(required=False, allow_none=True)
    max = FloatOrDateField(required=False, allow_none=True)


class SortSchema(BaseSchema):
    """Schema for validating sorting parameters."""

    column_name = ColumnField(required=False)
    desc = fields.Boolean(required=False)
    default_sort = fields.Integer(required=False, load_default=None, allow_none=True)
    table_id = fields.String(required=True)
    table = TableField(required=False)

    @pre_load
    def pre_load_data(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        # add default values to the data
        c_names = data.pop("id", "").split("_")

        table_id = data.get("table_id", None)
        data["table"] = self.get_table(table_id)

        if len(c_names) > 1:
            data["column_name"] = [
                to_snake_case_key(name.strip()) for name in c_names if name.strip()
            ]
        else:
            data["column_name"] = to_snake_case_key(c_names[0].strip())

            column_obj = next(
                (
                    col
                    for col in data["table"].__table__.columns
                    if col.name == data["column_name"]
                ),
                None,
            )

            if column_obj is None and data["column_name"] in ALISA_NAME:
                alias_column = ALISA_NAME[data["column_name"]]
                data["column_name"] = alias_column["key"]
                data["default_sort"] = alias_column["default"]

        return data

    @post_load
    def post_load_data(
        self, data: SortDict, **kwargs: Any
    ) -> Union[True_, UnaryExpression[Any], List[UnaryExpression[Any]]]:
        # add default values to the data
        sort: Union[True_, UnaryExpression[Any], List[UnaryExpression[Any]]] = true()
        if "table" in data and data["table"] is not None:
            sort = self.sort_data(
                data["table"], data["column_name"], data["desc"], data["default_sort"]
            )

        return sort


class FilterSchema(BaseSchema):
    """Schema for validating filter parameters."""

    column_name = ColumnField(required=False, load_default=None, allow_none=True)
    defalut_filter = fields.Integer(required=False, load_default=None, allow_none=True)
    filter_id = fields.String(required=False, load_default=None, allow_none=True)
    table_id = fields.String(required=True)
    table = TableField(required=True)
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
        c_names = data.pop("id", "").split("_")

        table_id = data.get("table_id", None)
        data["table"] = self.get_table(table_id)

        if len(c_names) > 1:
            data["column_name"] = [
                to_snake_case_key(name.strip()) for name in c_names if name.strip()
            ]
        else:
            data["column_name"] = to_snake_case_key(c_names[0].strip())

            column_obj = next(
                (
                    col
                    for col in data["table"].__table__.columns
                    if col.name == data["column_name"]
                ),
                None,
            )

            if column_obj is None and data["column_name"] in ALISA_NAME:
                alias_column = ALISA_NAME[data["column_name"]]
                data["column_name"] = alias_column["key"]
                data["defalut_filter"] = alias_column["default"]

        value = data.get("value", None)

        data["value"] = self.update_list_value(
            value, data["table"], data["column_name"]
        )

        return data

    @post_load
    def post_load_data(
        self, data: FilterDict, **kwargs: Any
    ) -> Union[True_, ColumnElement[Any], List[ColumnElement[Any]]]:
        filter: Union[True_, ColumnElement[Any], List[ColumnElement[Any]]] = (
            true()
        )  # Default filter to true (no filter)

        if "table" in data and data["table"] is not None:
            filter = self.filter_data(
                data["table"],
                data["column_name"],
                data["operator"],
                data["value"],
                data["range"],
                data["defalut_filter"],
            )

        return filter


class ParamSchema(BaseSchema):
    """Schema for validating parameters."""

    filter_flag = fields.String(required=False)

    filters = fields.List(
        fields.Nested(FilterSchema),
        required=False,
        load_default=[],
        allow_none=True,
    )
    sort = fields.List(fields.Nested(SortSchema), required=False, load_default=[])
    join_operator = JoinOperatorField(required=False, load_default=and_)

    page = fields.Integer(required=False, load_default=1)
    per_page = fields.Integer(required=False, load_default=10)

    @post_load
    def flatten_nested_list(self, data: PostLoadParam, **kwargs: Any) -> PostLoadParam:
        # Flatten list of lists
        if any(isinstance(item, list) for item in data["sort"]):
            flat_sort = []
            for sub_sort in data["sort"]:
                if isinstance(sub_sort, list):
                    flat_sort.extend(sub_sort)
                else:
                    flat_sort.append(sub_sort)
            data["sort"] = flat_sort
        if any(isinstance(item, list) for item in data["filters"]):
            flat_filter = []
            for sub_filter in data["filters"]:
                if isinstance(sub_filter, list):
                    flat_filter.extend(sub_filter)
                else:
                    flat_filter.append(sub_filter)
            data["filters"] = flat_filter

        return data


class STUDYearRecordSchema(BaseSchema):
    user_id = fields.String()
    grade_id = fields.String()

    year = fields.String()
    year_id = fields.String()

    final_score = DecimalEncoder(dump_default=None, allow_none=True)
    rank = fields.Integer(dump_default=None, allow_none=True)

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


class SectionPerSemesterSchema(BaseSchema):
    section_semester_one = fields.String(dump_default=None, allow_none=True)
    section_semester_two = fields.String(dump_default=None, allow_none=True)

    table_id = fields.String(required=False)

    @post_dump
    def add_fields(self, data, **kwargs: Any):
        """Add table_id to the dumped data."""
        data["table_id"] = self.get_table_id(Section)
        return data


class AveragePerSemesterSchema(BaseSchema):
    average_semester_one = DecimalEncoder(dump_default=None, allow_none=True)
    average_semester_two = DecimalEncoder(dump_default=None, allow_none=True)

    table_id = fields.String(required=False)

    @post_dump
    def add_fields(self, data, **kwargs: Any):
        """Add table_id to the dumped data."""
        data["table_id"] = self.get_table_id(STUDSemesterRecord)
        return data


class RankPerSemesterSchema(BaseSchema):
    rank_semester_one = fields.Integer(dump_default=None, allow_none=True)
    rank_semester_two = fields.Integer(dump_default=None, allow_none=True)

    table_id = fields.String(required=False)

    @post_dump
    def add_fields(self, data, **kwargs: Any):
        """Add table_id to the dumped data."""
        data["table_id"] = self.get_table_id(STUDSemesterRecord)
        return data


class PerSemesterSchema(BaseSchema):
    semester_one = fields.Integer(dump_default=None, allow_none=True)
    semester_two = fields.Integer(dump_default=None, allow_none=True)

    table_id = fields.String(required=False)

    @post_dump
    def add_fields(self, data, **kwargs: Any):
        """Add table_id to the dumped data."""
        data["table_id"] = self.get_table_id(Semester)
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
    sections = fields.Nested(SectionPerSemesterSchema, required=False, allow_none=True)
    averages = fields.Nested(AveragePerSemesterSchema, required=False, allow_none=True)
    ranks = fields.Nested(RankPerSemesterSchema, required=False, allow_none=True)

    semesters = fields.Nested(PerSemesterSchema, required=False, allow_none=True)

    year_record = fields.Nested(
        STUDYearRecordSchema(only=("final_score", "rank")),
        required=False,
        allow_none=False,
    )
