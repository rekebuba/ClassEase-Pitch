from typing import Set, Tuple
from flask import Response
from api.v1.utils.parameter import validate_fields
from api.v1.utils.typing import UserT
from api.v1.views.shared import auths as auth
from api.v1.views.utils import student_teacher_or_admin_required
from extension.pydantic.response.schema import success_response
from models import storage
from models.year import Year
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from extension.pydantic.models.year_schema import YearSchema
from api.v1.views import errors


@auth.route("/years", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(YearSchema, YearSchema.default_fields())
def get_years(user: UserT, fields: Set[str]) -> Tuple[Response, int]:
    """
    Returns a list of all academic years in the system.
    """
    try:
        years = storage.session.scalars(select(Year)).all()

        year_schemas = [YearSchema.model_validate(year) for year in years]
        valid_years = [
            schema.model_dump(by_alias=True, include=fields, mode="json")
            for schema in year_schemas
        ]

        return success_response(data=valid_years)

    except SQLAlchemyError as e:
        storage.session.rollback()
        return errors.handle_database_error(error=e)
    except Exception as e:
        storage.session.rollback()
        return errors.handle_internal_error(error=e)


@auth.route("/years/<string:year_id>", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(YearSchema, YearSchema.default_fields())
def get_year_by_id(user: UserT, fields: Set[str], year_id: str) -> Tuple[Response, int]:
    """
    Returns specific academic year
    """
    try:
        year = storage.session.get(Year, year_id)
        if not year:
            return errors.handle_not_found_error(message=f"Year with ID {year_id} not found.")

        year_schema = YearSchema.model_validate(year)
        valid_year = year_schema.model_dump(by_alias=True, include=fields, mode="json")

        return success_response(data=valid_year)

    except SQLAlchemyError as e:
        storage.session.rollback()
        return errors.handle_database_error(error=e)
    except Exception as e:
        storage.session.rollback()
        return errors.handle_internal_error(error=e)
