import logging
from typing import List, Tuple
import uuid
from flask import Response, request
from sqlalchemy import select
from api.v1.utils.typing import UserT
from api.v1.views.admin import admins as admin
from api.v1.views.admin.academic_year.schema import AcademicYearSetupSchema
from api.v1.views.utils import admin_required
from sqlalchemy.exc import SQLAlchemyError
from extension.pydantic.response.schema import error_response, success_response
from models import storage
from models.academic_term import AcademicTerm
from models.grade import Grade
from models.section import Section
from models.stream import Stream
from models.subject import Subject
from models.year import Year


def generate_subject_code(subject: str) -> str:
    # Split the subject name into words
    words = subject.split()

    # Determine the length of the prefix for each word (2 letters if multiple words, 3 otherwise)
    prefix_length = 3

    # Generate the base code by taking the first 'prefix_length' characters of each word and converting them to uppercase
    code = "".join(
        [
            word[:prefix_length].upper()
            for word in words
            if word.isalpha() and word != "and"
        ]
    )
    return code


@admin.route("/academic_year/setup", methods=["POST"])
@admin_required
def set_up_academic_year(user: UserT) -> Tuple[Response, int]:
    """
    Set up a complete academic year with terms, grades, sections, streams, and subjects.

    This operation is atomic - if any part fails, the entire transaction is rolled back.

    Args:
        user: Authenticated admin user

    Returns:
        Response with success message or error details
    """
    try:
        # Validate input data using Pydantic schema
        schema = AcademicYearSetupSchema.model_validate(request.json)

        # Create academic year
        year = Year(
            name=schema.year.name,
            calendar_type=schema.year.calendar_type,
            start_date=schema.year.start_date,
            end_date=schema.year.end_date,
            status=schema.year.status,
        )
        storage.session.add(year)
        storage.session.flush()  # Get the year.id immediately

        # Create academic terms
        academic_terms = []
        for term in schema.academic_term:
            academic_term = AcademicTerm(
                year_id=year.id,
                name=term.name,
                start_date=term.start_date,
                end_date=term.end_date,
                registration_start=term.registration_start,
                registration_end=term.registration_end,
            )
            academic_terms.append(academic_term)
        storage.session.add_all(academic_terms)

        subjects: List[Subject] = []
        for subj in schema.subjects:
            new_subject = Subject(
                year_id=year.id,
                name=subj,
                code=generate_subject_code(subj),
            )
            subjects.append(new_subject)

        storage.session.add_all(subjects)
        storage.session.flush()

        # Create grades with sections, subjects and streams
        for grade_data in schema.grades:
            # Create grade
            grade = Grade(
                year_id=year.id,
                level=grade_data.level,
                grade=grade_data.grade,
                has_stream=grade_data.has_stream,
            )
            storage.session.add(grade)
            storage.session.flush()

            # Add sections to grade
            sections = [
                Section(grade_id=grade.id, section=section_name)
                for section_name in grade_data.sections
            ]
            storage.session.add_all(sections)

            # Add subjects to grade
            for subject_name in grade_data.subjects:
                subject = storage.session.scalar(
                    select(Subject).where(Subject.name == subject_name)
                )
                if not subject:
                    raise ValueError(f"Subject '{subject_name}' not found")
                grade.subjects.append(subject)

            # Add streams if exists
            if grade_data.streams:
                for stream_data in grade_data.streams:
                    stream = Stream(
                        grade_id=grade.id,
                        name=stream_data.name,
                    )
                    storage.session.add(stream)
                    storage.session.flush()

                    # Add subjects to stream
                    for subject_name in stream_data.subjects:
                        subject = storage.session.scalar(
                            select(Subject).where(Subject.name == subject_name)
                        )
                        if not subject:
                            raise ValueError(
                                f"Stream subject '{subject_name}' not found"
                            )
                        stream.subjects.append(subject)

        # Commit all changes
        storage.session.commit()

        return success_response(
            message="Academic year setup completed successfully.",
            data={
                "year_id": year.id,
                "year_name": year.name,
                "start_date": year.start_date.isoformat(),
                "end_date": year.end_date.isoformat(),
            },
            status=201,
        )

    except ValueError as ve:
        storage.session.rollback()
        logging.error(f"Value Error: {ve}")
        return error_response(
            message="Validation error in academic year setup",
            status=400,
        )
    except SQLAlchemyError as se:
        storage.session.rollback()
        logging.error(f"Value Error: {se}")
        return error_response(
            message="Database error occurred during academic year setup",
            status=500,
        )
    except Exception as e:
        storage.session.rollback()
        logging.error(f"Value Error: {e}")
        return error_response(
            message="Unexpected error occurred during academic year setup",
            status=500,
        )


@admin.route("/academic_year/setup/<uuid:year_id>", methods=["DELETE"])
@admin_required
def delete_academic_year(user: UserT, year_id: uuid.UUID) -> Tuple[Response, int]:
    """
    Delete an academic year and all associated records.

    Args:
        year_id: ID of the academic year to delete
        user: Authenticated admin user
    Returns:
        Response with success message or error details
    """
    year = storage.session.scalar(select(Year).where(Year.id == year_id))
    if not year:
        return error_response(
            message="Academic year not found",
            status=404,
        )

    storage.session.delete(year)
    storage.session.commit()

    return success_response(
        message="Academic year deleted successfully.",
        data={"id": str(year_id)},
        status=200,
    )
