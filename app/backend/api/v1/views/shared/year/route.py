from typing import Tuple
from flask import Response
from api.v1.utils.typing import UserT
from api.v1.views.shared import auths as auth
from api.v1.views.utils import student_teacher_or_admin_required
from models import storage
from models.year import Year
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify
from extension.pydantic.models.year_schema import YearSchema
from api.v1.views import errors


@auth.route("/academic_years", methods=["GET"])
@student_teacher_or_admin_required
def get_years(user: UserT) -> Tuple[Response, int]:
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


@auth.route("/academic_year/<string:year_id>", methods=["GET"])
@student_teacher_or_admin_required
def get_year_by_id(user: UserT, year_id: str) -> Tuple[Response, int]:
    """
    Returns specific academic year
    """
    try:
        year = storage.session.scalar(select(Year).where(Year.id == year_id))

        year_schema = YearSchema.model_validate(year)
        response = year_schema.model_dump(by_alias=True)

        return jsonify(response), 200

    except SQLAlchemyError as e:
        storage.session.rollback()
        return errors.handle_database_error(e)
    except Exception as e:
        storage.session.rollback()
        return errors.handle_internal_error(e)
