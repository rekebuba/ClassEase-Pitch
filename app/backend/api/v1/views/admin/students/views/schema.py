from api.v1.schemas.base_schema import BaseSchema
from marshmallow import EXCLUDE, fields

from api.v1.schemas.config_schema import OPERATOR_CONFIG
from api.v1.schemas.custom_schema import EnumField, ValueField
from models import storage
from models.base_model import CustomTypes
from models.saved_query_view import SavedQueryView
from models.table import Table


class FilterSchema(BaseSchema):
    """Schema for validating filter parameters."""

    class Meta:
        unknown = EXCLUDE

    id = fields.String(required=True)
    table_id = fields.String(
        required=True,
        validate=lambda x: storage.session.query(Table).filter_by(id=x).count() == 1,
    )
    variant = fields.String(
        validate=lambda x: x
        in ["text", "number", "multiSelect", "boolean", "date", "dateRange", "range"],
        required=True,
    )
    operator = fields.String(required=True, validate=lambda x: x in OPERATOR_CONFIG)
    value = ValueField(required=False, load_default=None, allow_none=True)


class SortSchema(BaseSchema):
    """Schema for validating sorting parameters."""

    id = fields.String(required=True)
    desc = fields.Boolean(required=False, load_default=False)
    table_id = fields.String(
        required=True,
        validate=lambda x: storage.session.query(Table).filter_by(id=x).count() == 1,
    )


class searchParamsSchema(BaseSchema):
    """Schema for validating search parameters."""

    filters = fields.List(
        fields.Nested(FilterSchema),
        required=False,
        load_default=[],
    )
    sort = fields.List(fields.Nested(SortSchema), required=False, load_default=[])
    join_operator = fields.String(
        required=False, load_default="and", validate=lambda x: x in ["and", "or"]
    )

    page = fields.Integer(required=False, load_default=1)
    per_page = fields.Integer(
        required=False, load_default=10, validate=lambda x: 1 <= x <= 50 and x % 10 == 0
    )


class ValidQuerySchema(BaseSchema):
    """
    Schema for validating query parameters for student views.
    """

    filter_flag = fields.String(required=False)
    view_id = fields.String(required=True)

    columns = fields.List(
        fields.String(),
        required=False,
        load_default=[],
    )
    name = fields.String(
        required=False, load_default="new View", validate=lambda x: len(x) <= 50
    )
    table_name = EnumField(CustomTypes.TableEnum, required=True)
    search_params = fields.Nested(
        searchParamsSchema,
        required=False,
        load_default={},
    )


class AllStudentViews(BaseSchema):
    view_id = fields.String()
    name = fields.String()
    table_name = fields.String()
    columns = fields.List(fields.String())
    search_params = fields.Dict(
        keys=fields.String(),
        values=fields.Raw(),
        required=False,
    )
    created_at = fields.DateTime(format="iso")
    updated_at = fields.DateTime(format="iso")
