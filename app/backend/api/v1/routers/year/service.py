import json
import logging
import uuid
from datetime import date
from typing import Dict, List, Union

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from api.v1.routers.year.schema import YearSetupTemplate
from models.academic_term import AcademicTerm
from models.grade import Grade
from models.grade_stream_subject import GradeStreamSubject
from models.section import Section
from models.stream import Stream
from models.subject import Subject
from utils.enum import AcademicTermEnum, AcademicTermTypeEnum
from utils.type import SetupMethodType


def create_academic_term(
    *,
    year_id: uuid.UUID,
    calendar_type: AcademicTermTypeEnum,
    session: Session,
) -> None:
    """
    Creates academic terms for a new academic year based on its calendar type.
    """
    num_terms = 2 if calendar_type == AcademicTermTypeEnum.SEMESTER else 4

    term_names = [enum for enum in AcademicTermEnum][:num_terms]

    terms_to_create = [
        AcademicTerm(
            year_id=year_id,
            name=term,
            start_date=date.today(),
            end_date=date.today(),
            registration_start=None,
            registration_end=None,
        )
        for term in term_names
    ]
    if terms_to_create:
        session.add_all(terms_to_create)


def handle_setup_methods(
    *,
    old_year_id: uuid.UUID | None,
    year_id: uuid.UUID,
    session: Session,
    setup_methods: SetupMethodType,
) -> None:
    """
    Handles the setup methods for creating a new academic year.
    """
    if setup_methods == "Default Template":
        # Implement the logic for setting up a default template
        _handle_default_template_setup(
            year_id=year_id,
            session=session,
        )
    elif setup_methods == "Last Year Copy":
        if old_year_id is None:
            raise ValueError("old_year_id must be provided for 'Last Year Copy'")

        _handle_year_copy_setup(
            old_year_id=old_year_id,
            year_id=year_id,
            session=session,
        )
    elif setup_methods == "Manual":
        pass
    else:
        raise ValueError("Invalid setup method")


def load_year_from_file(path: str) -> YearSetupTemplate:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)[0]
    # Validate using Pydantic
    return YearSetupTemplate(**data)


def _handle_default_template_setup(
    *,
    year_id: uuid.UUID,
    session: Session,
) -> None:
    """
    Handles the default template setup for a new academic year.
    """
    try:
        template = load_year_from_file("./template/default_academic_year.json")
    except Exception as e:
        logging.error(f"Error loading default academic year template: {e}")
        raise

    try:
        all_objects_to_add: List[
            Union[Subject, Grade, Section, GradeStreamSubject, Stream]
        ] = []

        # Create subjects
        subject_map: Dict[str, Subject] = {}
        for s in template.subjects:
            new_subject = Subject(name=s.name, code=s.code, year_id=year_id)
            subject_map[s.name] = new_subject
            all_objects_to_add.append(new_subject)

        # Add subjects first to get their IDs
        session.add_all(all_objects_to_add)
        session.flush()
        all_objects_to_add.clear()  # Reset for next batch

        # Process grades
        for grade_data in template.grades:
            grade = Grade(
                year_id=year_id,
                level=grade_data.level,
                grade=grade_data.grade,
                has_stream=grade_data.has_stream,
            )
            all_objects_to_add.append(grade)

            # Add grade and flush to get ID
            session.add_all(all_objects_to_add)
            session.flush()
            all_objects_to_add.clear()

            # Create sections
            sections = [
                Section(grade_id=grade.id, section=section.section)
                for section in template.sections
            ]
            all_objects_to_add.extend(sections)

            # Add non-streamed subjects
            for subj in grade_data.subjects:
                subject = subject_map.get(subj.name)
                if not subject:
                    raise ValueError(f"Subject '{subj.name}' not found")
                all_objects_to_add.append(
                    GradeStreamSubject(
                        grade_id=grade.id,
                        stream_id=None,
                        subject_id=subject.id,
                    )
                )

            # Process streams
            if grade_data.streams:
                streams = []
                for stream_data in grade_data.streams:
                    stream = Stream(grade_id=grade.id, name=stream_data.name)
                    streams.append(stream)
                    all_objects_to_add.append(stream)

                # Add streams and flush to get IDs
                session.add_all(all_objects_to_add)
                session.flush()
                all_objects_to_add.clear()

                # Add stream subjects
                for stream_data, stream in zip(grade_data.streams, streams):
                    for subj in stream_data.subjects:
                        subject = subject_map.get(subj.name)
                        if not subject:
                            raise ValueError(f"Subject '{subj.name}' not found")
                        all_objects_to_add.append(
                            GradeStreamSubject(
                                grade_id=grade.id,
                                stream_id=stream.id,
                                subject_id=subject.id,
                            )
                        )

            # Add remaining objects for this grade
            if all_objects_to_add:
                session.add_all(all_objects_to_add)
                session.flush()
                all_objects_to_add.clear()

    except Exception:
        # The calling function will handle rollback
        raise


def _handle_year_copy_setup(
    *,
    old_year_id: uuid.UUID,
    year_id: uuid.UUID,
    session: Session,
) -> None:
    """
    Handles copying an existing academic year's setup to a new year.
    This is optimized to perform batch inserts and avoid N+1 query problems.
    """
    try:
        # 1. Fetch all required data from the old year in bulk,
        # eager loading relationships
        old_subjects = session.scalars(
            select(Subject).where(Subject.year_id == old_year_id)
        ).all()
        old_grades = session.scalars(
            select(Grade)
            .where(Grade.year_id == old_year_id)
            .options(selectinload(Grade.sections), selectinload(Grade.streams))
        ).all()
        old_gss_items = session.scalars(
            select(GradeStreamSubject).join(Grade).where(Grade.year_id == old_year_id)
        ).all()

        # 2. Create new objects in memory and map old IDs to new objects
        subject_mapping: Dict[uuid.UUID, Subject] = {}
        new_subjects: List[Subject] = []
        for old_subject in old_subjects:
            new_subject = Subject(
                name=old_subject.name, code=old_subject.code, year_id=year_id
            )
            subject_mapping[old_subject.id] = new_subject
            new_subjects.append(new_subject)

        session.add_all(new_subjects)
        session.flush()

        grade_mapping: Dict[uuid.UUID, Grade] = {}
        new_grades: List[Grade] = []
        for old_grade in old_grades:
            new_grade = Grade(
                year_id=year_id,
                level=old_grade.level,
                grade=old_grade.grade,
                has_stream=old_grade.has_stream,
            )
            grade_mapping[old_grade.id] = new_grade
            new_grades.append(new_grade)

        session.add_all(new_grades)
        session.flush()

        new_sections: List[Section] = []
        new_streams: List[Stream] = []
        stream_mapping: Dict[uuid.UUID, Stream] = {}
        for old_grade in old_grades:
            new_grade = grade_mapping[old_grade.id]

            # Copy sections
            for old_section in old_grade.sections:
                new_sections.append(
                    Section(grade_id=new_grade.id, section=old_section.section)
                )

            # Copy streams
            for old_stream in old_grade.streams:
                new_stream = Stream(grade_id=new_grade.id, name=old_stream.name)
                stream_mapping[old_stream.id] = new_stream
                new_streams.append(new_stream)

        session.add_all(new_sections)
        session.add_all(new_streams)
        session.flush()

        # 3. Re-create GradeStreamSubject relationships using the new objects
        new_gss_items: List[GradeStreamSubject] = []
        for old_gss in old_gss_items:
            new_subject_gss = subject_mapping.get(old_gss.subject_id)
            new_grade_gss = grade_mapping.get(old_gss.grade_id)

            if not new_subject_gss:
                raise ValueError(
                    f"Subject ID '{old_gss.subject_id}' not found in subject mapping"
                )
            if not new_grade_gss:
                raise ValueError(
                    f"Grade ID '{old_gss.grade_id}' not found in grade mapping"
                )

            new_stream_gss: Stream | None = None
            if old_gss.stream_id:
                new_stream_gss = stream_mapping.get(old_gss.stream_id)
                if not new_stream_gss:
                    raise ValueError(
                        f"Stream ID '{old_gss.stream_id}' not found in stream mapping"
                    )

            new_gss_items.append(
                GradeStreamSubject(
                    grade_id=new_grade_gss.id,
                    stream_id=new_stream_gss.id if new_stream_gss else None,
                    subject_id=new_subject_gss.id,
                )
            )

        # 4. Add all new objects to the session at once
        session.add_all(new_gss_items)

    except Exception:
        # The calling function will handle rollback
        raise
