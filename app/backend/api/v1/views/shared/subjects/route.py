from typing import Tuple
from sqlalchemy import select
from api.v1.views import errors
from api.v1.views.shared import auths as auth
from extension.pydantic.models.grade_schema import GradeSchema
from extension.pydantic.models.subject_schema import SubjectSchema
from models import storage
from models.grade import Grade
from models.subject import Subject
from sqlalchemy.exc import SQLAlchemyError
from flask import Response, jsonify

from models.yearly_subject import YearlySubject


@auth.route("/subjects", methods=["GET"])
def get_available_subjects() -> Tuple[Response, int]:
    """
    Returns a list of all available subjects in the system.
    """
    try:
        subjects = storage.session.scalars(select(Subject)).all()

        subject_schemas = [
            SubjectSchema.model_validate(subject) for subject in subjects
        ]
        valid_subjects = [
            schema.model_dump(by_alias=True) for schema in subject_schemas
        ]
        return jsonify(valid_subjects), 200

    except SQLAlchemyError as e:
        storage.session.rollback()
        return errors.handle_database_error(e)
    except Exception as e:
        storage.session.rollback()
        return errors.handle_internal_error(e)


@auth.route("/subjects/<subject_id>", methods=["GET"])
def get_subject_by_id(subject_id: str) -> Tuple[Response, int]:
    """Returns Subject model based on subject_id"""
    try:
        subject = storage.session.get(Subject, subject_id)
        if not subject:
            return jsonify({"error": "Subject not found"}), 404

        subject_schema = SubjectSchema.model_validate(subject)
        valid_subject = subject_schema.model_dump(by_alias=True)

        return jsonify(valid_subject), 200

    except SQLAlchemyError as e:
        storage.session.rollback()
        return errors.handle_database_error(e)
    except Exception as e:
        storage.session.rollback()
        return errors.handle_internal_error(e)


@auth.route("/subjects/<subject_id>/grades", methods=["GET"])
def get_subject_grade(subject_id: str) -> Tuple[Response, int]:
    """
    Returns the grades associated with a specific subject.
    """
    try:
        grades = storage.session.scalars(
            select(Grade)
            .select_from(YearlySubject)
            .join(Subject, Subject.id == YearlySubject.subject_id)
            .join(Grade, Grade.id == YearlySubject.grade_id)
            .where(Subject.id == subject_id)
        ).all()

        if not grades:
            return errors.handle_not_found_error(
                f"Subject with id {subject_id} not found."
            )

        grade_schemas = [GradeSchema.model_validate(grade) for grade in grades]
        valid_grades = [schema.model_dump(by_alias=True) for schema in grade_schemas]

        return jsonify(valid_grades), 200

    except SQLAlchemyError as e:
        storage.session.rollback()
        return errors.handle_database_error(e)
    except Exception as e:
        storage.session.rollback()
        return errors.handle_internal_error(e)
