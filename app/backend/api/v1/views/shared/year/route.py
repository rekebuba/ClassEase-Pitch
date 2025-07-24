from typing import Set, Tuple
import uuid
from flask import Response
from api.v1.utils.parameter import validate_expand, validate_fields
from api.v1.utils.typing import IncEx, UserT
from api.v1.views.shared import auths as auth
from api.v1.views.utils import student_teacher_or_admin_required
from extension.pydantic.response.schema import success_response
from models import storage
from models.year import Year
from sqlalchemy import select
from extension.pydantic.models.year_schema import (
    YearRelationshipSchema,
    YearSchema,
    YearSchemaWithRelationships,
)
from api.v1.views import errors


@auth.route("/years", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(YearSchema, YearSchema.default_fields())
def get_years(user: UserT, fields: Set[str]) -> Tuple[Response, int]:
    """
    Returns a list of all academic years in the system.
    """
    years = storage.session.scalars(select(Year)).all()

    year_schemas = [YearSchema.model_validate(year) for year in years]
    valid_years = [
        schema.model_dump(by_alias=True, include=fields, mode="json")
        for schema in year_schemas
    ]

    return success_response(data=valid_years)


@auth.route("/years/<uuid:year_id>", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(YearSchema, YearSchema.default_fields())
@validate_expand(YearRelationshipSchema)
def get_year_by_id(
    user: UserT,
    fields: dict[str, IncEx],
    related_fields: dict[str, IncEx],
    year_id: uuid.UUID,
) -> Tuple[Response, int]:
    """
    Returns specific academic year
    """
    year = storage.session.get(Year, year_id)
    if not year:
        return errors.handle_not_found_error(
            message=f"Year with ID {year_id} not found."
        )

    response = YearSchemaWithRelationships.model_validate(year).model_dump(
        by_alias=True,
        include={
            **fields,
            **related_fields,
        },
        mode="json",
    )

    return success_response(data=response)
