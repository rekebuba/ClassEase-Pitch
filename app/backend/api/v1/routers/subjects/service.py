import uuid
from typing import List, Sequence

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from api.v1.routers.subjects.schema import (
    UpdateSubjectGrade,
    UpdateSubjectSetup,
    UpdateSubjectStream,
)
from models.grade import Grade
from models.grade_stream_subject import GradeStreamSubject
from models.stream import Stream
from models.subject import Subject


def update_subject_relationships(
    subject: Subject, update_data: UpdateSubjectSetup, session: Session
) -> None:
    """
    Update subject relationships (streams and grades) efficiently.

    This function handles the complex relationship updates for a Subject object,
    including creating new , updating existing ones, and removing
    deleted relationships while minimizing database queries.

    Args:
        subject: The Subject ORM object to update
        update_data: Pydantic schema containing updated relationship data
        session: SQLAlchemy session for database operations

    Raises:
        ValueError: If invalid data is provided
        SQLAlchemyError: If database operations fail
    """
    try:
        # --- STREAMS UPDATE ---
        if (
            "streams" in update_data.model_fields_set
            and update_data.streams is not None
        ):
            _update_subject_streams(
                subject=subject,
                new_streams=update_data.streams,
                session=session,
            )

        # --- GRADES UPDATE ---
        if "grades" in update_data.model_fields_set and update_data.grades is not None:
            existing_grades = session.scalars(
                select(Grade)
                .join(GradeStreamSubject)
                .where(
                    GradeStreamSubject.subject_id == subject.id,
                    GradeStreamSubject.stream_id == None,  # noqa: E711
                )
            ).all()
            _update_subject_grades(
                subject=subject,
                new_grades=update_data.grades,
                session=session,
                existing_grades=existing_grades,
                stream_id=None,
            )

        session.flush()  # Batch all changes before commit
    except Exception as e:
        session.rollback()
        raise e


def _update_subject_streams(
    *,
    subject: Subject,
    new_streams: List[UpdateSubjectStream],
    session: Session,
) -> None:
    """
    Updates the streams associated with a subject using bulk operations.
    """
    # Get existing stream associations for this subject
    existing_gss_items = session.scalars(
        select(GradeStreamSubject).where(
            GradeStreamSubject.subject_id == subject.id,
            GradeStreamSubject.stream_id.isnot(None),
        )
    ).all()

    # Create mapping for efficient lookup
    existing_associations = {
        (gss.grade_id, gss.stream_id): gss.id for gss in existing_gss_items
    }

    # Get new associations from the input
    new_associations = {(s.grade_id, s.id) for s in new_streams}

    # Determine what to add and what to remove
    associations_to_add = new_associations - existing_associations.keys()
    associations_to_remove = set(existing_associations.keys()) - new_associations

    # Validate new associations exist
    if associations_to_add:
        _validate_grade_stream_associations(associations_to_add, session)

    # Bulk add new associations
    if associations_to_add:
        session.add_all(
            [
                GradeStreamSubject(
                    subject_id=subject.id, grade_id=grade_id, stream_id=stream_id
                )
                for grade_id, stream_id in associations_to_add
            ]
        )

    # Bulk remove old associations
    if associations_to_remove:
        gss_to_delete_ids = [
            existing_associations[assoc] for assoc in associations_to_remove
        ]
        stmt = delete(GradeStreamSubject).where(
            GradeStreamSubject.id.in_(gss_to_delete_ids)
        )
        session.execute(stmt)


def _update_subject_grades(
    *,
    subject: Subject,
    new_grades: List[UpdateSubjectGrade],
    session: Session,
    existing_grades: Sequence[Grade],
    stream_id: uuid.UUID | None,
) -> None:
    """
    Update subject grades relationship efficiently for non-streamed grades.

    Replaces the current grades with the new list, handling both
    additions and removals in a single operation.
    """
    existing_grade_ids = {grade.id for grade in existing_grades}
    new_grade_ids = {grade.id for grade in new_grades}

    # Determine which grades to add and which to remove
    grade_ids_to_add = new_grade_ids - existing_grade_ids
    grade_ids_to_remove = existing_grade_ids - new_grade_ids

    # Validate grades exist
    if grade_ids_to_add:
        _validate_grades_exist(grade_ids_to_add, session)

        session.add_all(
            [
                GradeStreamSubject(
                    grade_id=grade_id,
                    subject_id=subject.id,
                    stream_id=stream_id,  # Will be None
                )
                for grade_id in grade_ids_to_add
            ]
        )

    # Bulk remove old grade relationships
    if grade_ids_to_remove:
        stmt = delete(GradeStreamSubject).where(
            GradeStreamSubject.subject_id == subject.id,
            GradeStreamSubject.stream_id == stream_id,
            GradeStreamSubject.grade_id.in_(grade_ids_to_remove),
        )
        session.execute(stmt)


def _validate_grade_stream_associations(
    associations: set[tuple[uuid.UUID, uuid.UUID]], session: Session
) -> None:
    """Validate that grade-stream combinations exist in the database."""
    grade_ids, stream_ids = zip(*associations) if associations else ([], [])

    existing_grades = session.scalars(
        select(Grade.id).where(Grade.id.in_(grade_ids))
    ).all()
    existing_streams = session.scalars(
        select(Stream.id).where(Stream.id.in_(stream_ids))
    ).all()

    missing_grades = set(grade_ids) - set(existing_grades)
    missing_streams = set(stream_ids) - set(existing_streams)

    if missing_grades or missing_streams:
        raise ValueError(
            f"Invalid grade-stream associations: "
            f"Missing grades: {missing_grades}, "
            f"Missing streams: {missing_streams}"
        )


def _validate_grades_exist(grade_ids: set[uuid.UUID], session: Session) -> None:
    """Validate that grades exist in the database."""
    if not grade_ids:
        return

    existing_grades = session.scalars(
        select(Grade.id).where(Grade.id.in_(grade_ids))
    ).all()

    missing_grades = grade_ids - set(existing_grades)

    if missing_grades:
        raise ValueError(f"Invalid grade IDs provided: {missing_grades}")
