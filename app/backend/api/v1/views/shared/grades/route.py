from typing import Tuple
from sqlalchemy import select
from api.v1.views import errors
from api.v1.views.shared import auths as auth
from extension.pydantic.models.grade_schema import GradeSchema
from models import storage
from models.grade import Grade
from sqlalchemy.exc import SQLAlchemyError
from flask import Response, jsonify


@auth.route("/grades", methods=["GET"])
def get_available_grades() -> Tuple[Response, int]:
    """
    Returns a list of all available grades in the system.
    """
    try:
        grades = storage.session.scalars(select(Grade)).all()

        grade_schemas = [GradeSchema.model_validate(grade) for grade in grades]
        valid_grades = [schema.model_dump(by_alias=True) for schema in grade_schemas]

        return jsonify(valid_grades), 200

    except SQLAlchemyError as e:
        storage.session.rollback()
        return errors.handle_database_error(e)
    except Exception as e:
        storage.session.rollback()
        return errors.handle_internal_error(e)


@auth.route("/grades/<grade_id>", methods=["GET"])
def get_grade_by_id(grade_id: str) -> Tuple[Response, int]:
    """Returns Grade model based on grade_id"""
    try:
        grade = storage.session.get(Grade, grade_id)
        if not grade:
            return jsonify({"error": "Grade not found"}), 404

        valid_grade = GradeSchema.model_validate(grade)

        return jsonify(valid_grade), 200

    except SQLAlchemyError as e:
        storage.session.rollback()
        return errors.handle_database_error(e)
    except Exception as e:
        storage.session.rollback()
        return errors.handle_internal_error(e)
