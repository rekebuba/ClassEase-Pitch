from typing import Any, Tuple
import uuid
from flask import Response
from api.v1.utils.test_parameter import query_parameters
from api.v1.utils.typing import UserT
from api.v1.views.shared import auths as auth
from api.v1.views.utils import student_teacher_or_admin_required
from extension.pydantic.response.schema import error_response, success_response
from models import storage
from models.year import Year
from sqlalchemy import select
from extension.pydantic.models.year_schema import (
    YearNestedSchema,
    YearSchema,
)


@auth.route("/years", methods=["GET"])
@student_teacher_or_admin_required
@query_parameters(YearNestedSchema)
def get_years(user: UserT, include_params: dict[str, Any]) -> Tuple[Response, int]:
    """
    Returns a list of all academic years in the system.
    """
    years = storage.session.scalars(select(Year)).all()

    year_schemas = [YearNestedSchema.model_validate(year) for year in years]
    valid_years = [
        schema.model_dump(by_alias=True, include=include_params, mode="json")
        for schema in year_schemas
    ]

    return success_response(data=valid_years)


@auth.route("/years/<uuid:year_id>", methods=["GET"])
@student_teacher_or_admin_required
@query_parameters(YearNestedSchema)
def get_year_by_id(
    user: UserT,
    include_params: dict[str, Any],
    year_id: uuid.UUID,
) -> Tuple[Response, int]:
    """
    Returns specific academic year
    """
    year = storage.session.get(Year, year_id)
    if not year:
        return error_response(message=f"Year with ID {year_id} not found.", status=404)

    response = YearNestedSchema.model_validate(year).model_dump(
        by_alias=True,
        include=include_params,
        mode="json",
    )

    return success_response(data=response)
