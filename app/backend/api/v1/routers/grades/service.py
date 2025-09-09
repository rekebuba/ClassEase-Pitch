import uuid
from typing import List, Sequence

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from api.v1.routers.grades.schema import (
    UpdateGradeSetup,
    UpdateSection,
    UpdateStreamSetup,
    UpdateSubject,
)
from models.grade import Grade
from models.grade_stream_subject import GradeStreamSubject
from models.section import Section
from models.stream import Stream
from models.subject import Subject


def update_grade_relationships(
    grade: Grade, update_data: UpdateGradeSetup, session: Session
) -> None:
    """
    Update grade relationships (subjects, streams, sections) efficiently.

    This function handles the complex relationship updates for a Grade object,
    including creating new entities, updating existing ones, and removing
    deleted relationships while minimizing database queries.

    Args:
        grade: The Grade ORM object to update
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
            _update_grade_streams(grade, update_data.streams, session)

        # --- SUBJECTS UPDATE ---
        elif (
            "subjects" in update_data.model_fields_set
            and update_data.subjects is not None
        ):
            existing_subjects = session.scalars(
                select(Subject)
                .join(GradeStreamSubject)
                .where(GradeStreamSubject.grade_id == grade.id)
            ).all()
            _update_grade_subjects(
                grade=grade,
                new_subjects=update_data.subjects,
                session=session,
                existing_subjects=existing_subjects,
                stream_id=None,
            )

        # --- SECTIONS UPDATE ---
        if (
            "sections" in update_data.model_fields_set
            and update_data.sections is not None
        ):
            _update_grade_sections(grade, update_data.sections, session)

        session.flush()  # Batch all changes before commit
    except Exception as e:
        session.rollback()
        raise e


def _update_grade_subjects(
    *,
    grade: Grade,
    new_subjects: List[UpdateSubject],
    session: Session,
    existing_subjects: Sequence[Subject],
    stream_id: uuid.UUID | None,
) -> None:
    """
    Update grade subjects relationship efficiently.

    Replaces the current subjects with the new list, handling both
    additions and removals in a single operation.
    """
    existing_subject_ids = {subject.id for subject in existing_subjects}
    new_subject_ids = {subject.id for subject in new_subjects}

    # Determine which subjects to add and which to remove
    subject_ids_to_add = new_subject_ids - existing_subject_ids
    subject_ids_to_remove = existing_subject_ids - new_subject_ids

    # Bulk add new subject relationships
    if subject_ids_to_add:
        session.add_all(
            [
                GradeStreamSubject(
                    grade_id=grade.id,
                    subject_id=subject_id,
                    stream_id=stream_id,
                )
                for subject_id in subject_ids_to_add
            ]
        )
    # Bulk remove old subject relationships
    if subject_ids_to_remove:
        stmt = delete(GradeStreamSubject).where(
            GradeStreamSubject.grade_id == grade.id,
            GradeStreamSubject.stream_id == stream_id,
            GradeStreamSubject.subject_id.in_(subject_ids_to_remove),
        )
        session.execute(stmt)


def _update_grade_streams(
    grade: Grade, new_streams: List[UpdateStreamSetup], session: Session
) -> None:
    """
    Update grade streams with their subjects.

    Handles:
    - Creating new streams with subjects
    - Updating existing stream subjects
    - Removing deleted streams
    """
    # 1. Fetch all existing data in bulk to avoid N+1 queries
    existing_streams = session.scalars(
        select(Stream).where(Stream.grade_id == grade.id)
    ).all()

    existing_streams_by_name = {s.name: s for s in existing_streams}
    new_streams_by_name = {s.name: s for s in new_streams if s.name}

    streams_to_add: List[tuple[Stream, List[UpdateSubject]]] = [
        (Stream(grade_id=grade.id, name=stream.name), stream.subjects)
        for stream in new_streams
        if stream.name and stream.name not in existing_streams_by_name
    ]

    streams_to_remove = [
        stream for stream in existing_streams if stream.name not in new_streams_by_name
    ]

    streams_to_update = [
        (existing_streams_by_name[stream.name], stream)
        for stream in new_streams
        if stream.name in existing_streams_by_name
    ]

    if streams_to_add:
        session.add_all([stream for stream, _ in streams_to_add])

    # Validate streams exist
    if streams_to_remove:
        stream_ids_to_remove = {s.id for s in streams_to_remove}
        _validate_streams_exist(stream_ids_to_remove, session)

        stmt = delete(Stream).where(
            Stream.id.in_(stream_ids_to_remove),
        )
        session.execute(stmt)

    session.flush()

    #  Add subjects for New streams
    for new_stream, new_subjects in streams_to_add:
        _update_grade_subjects(
            grade=grade,
            new_subjects=new_subjects,
            session=session,
            existing_subjects=[],
            stream_id=new_stream.id,
        )

    #  Update subjects for existing streams
    for existing_stream, new_stream_data in streams_to_update:
        _update_grade_subjects(
            grade=grade,
            new_subjects=new_stream_data.subjects,
            session=session,
            existing_subjects=existing_stream.subjects,
            stream_id=existing_stream.id,
        )


def _update_grade_sections(
    grade: Grade, new_sections: List[UpdateSection], session: Session
) -> None:
    """
    Update grade sections relationship.

    Handles creation of new sections and removal of deleted ones.
    """
    # Batch load existing sections
    existing_sections = session.scalars(
        select(Section).where(Section.grade_id == grade.id)
    ).all()

    existing_sections_by_name = {s.section: s for s in existing_sections}
    new_sections_by_name = {s.section: s for s in new_sections if s.section}

    sections_to_add: List[Section] = [
        Section(grade_id=grade.id, section=section.section)
        for section in new_sections
        if section.section and section.section not in existing_sections_by_name
    ]

    sections_to_remove = [
        section
        for section in existing_sections
        if section.section not in new_sections_by_name
    ]

    if sections_to_add:
        session.add_all(sections_to_add)

    # Validate sections exist
    if sections_to_remove:
        section_ids_to_remove = {s.id for s in sections_to_remove}
        _validate_sections_exist(section_ids_to_remove, session)

        stmt = delete(Section).where(
            Section.id.in_(section_ids_to_remove),
        )
        session.execute(stmt)


def _validate_streams_exist(stream_ids: set[uuid.UUID], session: Session) -> None:
    """Validate that Stream ids exist in the database."""
    if not stream_ids:
        return

    existing_streams = session.scalars(
        select(Stream.id).where(Stream.id.in_(stream_ids))
    ).all()

    missing_streams = stream_ids - set(existing_streams)

    if missing_streams:
        raise ValueError(f"Invalid stream IDs provided: {missing_streams}")


def _validate_sections_exist(section_ids: set[uuid.UUID], session: Session) -> None:
    """Validate that Section ids exist in the database."""
    if not section_ids:
        return

    existing_sections = session.scalars(
        select(Section.id).where(Section.id.in_(section_ids))
    ).all()

    missing_sections = section_ids - set(existing_sections)

    if missing_sections:
        raise ValueError(f"Invalid Section IDs provided: {missing_sections}")
