from typing import Tuple
from flask import Response
from api.v1.views.shared import auths as auth
from models import storage
from models.year import Year
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify
from extension.pydantic.models.year_schema import YearSchema
from api.v1.views import errors


@auth.route("/academic_years", methods=["GET"])
def get_years() -> Tuple[Response, int]:
    """
    Returns a list of all academic years in the system.
    """
    try:
        years = storage.session.scalars(select(Year)).all()

        year_schemas = [YearSchema.model_validate(year) for year in years]
        valid_years = [schema.model_dump(by_alias=True) for schema in year_schemas]

        return jsonify(valid_years), 200

    except SQLAlchemyError as e:
        storage.session.rollback()
        return errors.handle_database_error(e)
    except Exception as e:
        storage.session.rollback()
        return errors.handle_internal_error(e)
