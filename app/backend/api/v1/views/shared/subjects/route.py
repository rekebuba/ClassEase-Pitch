from typing import Set, Tuple
import uuid
from sqlalchemy import select
from api.v1.utils.parameter import validate_fields
from api.v1.utils.typing import UserT
from api.v1.views import errors
from api.v1.views.shared import auths as auth
from api.v1.views.utils import student_teacher_or_admin_required
from extension.pydantic.models.grade_schema import GradeSchema
from extension.pydantic.models.subject_schema import SubjectSchema
from extension.pydantic.response.schema import success_response
from models import storage
from models.grade import Grade
from models.subject import Subject
from sqlalchemy.exc import SQLAlchemyError
from flask import Response, jsonify

from models.yearly_subject import YearlySubject


@auth.route("/years/<uuid:year_id>/subjects", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(SubjectSchema, SubjectSchema.default_fields())
def get_available_subjects(
    user: UserT, fields: Set[str], year_id: uuid.UUID
) -> Tuple[Response, int]:
    """
    Returns a list of all available subjects in the system.
    """
    try:
        subjects = storage.session.scalars(
            select(Subject).where(Subject.year_id == year_id)
        ).all()

        subject_schemas = [
            SubjectSchema.model_validate(subject) for subject in subjects
        ]
        valid_subjects = [
            schema.model_dump(by_alias=True, include=fields)
            for schema in subject_schemas
        ]
        return success_response(data=valid_subjects)

    except SQLAlchemyError as e:
        storage.session.rollback()
        return errors.handle_database_error(error=e)
    except Exception as e:
        storage.session.rollback()
        return errors.handle_internal_error(error=e)


@auth.route("/years/<uuid:year_id>/subjects/<uuid:subject_id>", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(SubjectSchema, SubjectSchema.default_fields())
def get_subject_by_id(
    user: UserT,
    fields: Set[str],
    year_id: uuid.UUID,
    subject_id: uuid.UUID,
) -> Tuple[Response, int]:
    """Returns Subject model based on subject_id"""
    try:
        subject = storage.session.scalar(
            select(Subject).where(Subject.id == subject_id, Subject.year_id == year_id)
        )
        if not subject:
            return jsonify({"error": "Subject not found"}), 404

        subject_schema = SubjectSchema.model_validate(subject)
        valid_subject = subject_schema.model_dump(by_alias=True, include=fields)

        return success_response(data=valid_subject)

    except SQLAlchemyError as e:
        storage.session.rollback()
        return errors.handle_database_error(error=e)
    except Exception as e:
        storage.session.rollback()
        return errors.handle_internal_error(error=e)


@auth.route("/subjects/<subject_id>/grades", methods=["GET"])
@student_teacher_or_admin_required
def get_subject_grade(user: UserT, subject_id: str) -> Tuple[Response, int]:
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
                message=f"Subject with id {subject_id} not found."
            )

        grade_schemas = [GradeSchema.model_validate(grade) for grade in grades]
        valid_grades = [schema.model_dump(by_alias=True) for schema in grade_schemas]

        return jsonify(valid_grades), 200

    except SQLAlchemyError as e:
        storage.session.rollback()
        return errors.handle_database_error(error=e)
    except Exception as e:
        storage.session.rollback()
        return errors.handle_internal_error(error=e)
