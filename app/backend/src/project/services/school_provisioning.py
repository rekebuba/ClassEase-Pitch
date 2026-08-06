"""Tenant blueprint provisioning service."""

import uuid
from dataclasses import dataclass
from datetime import date
from typing import Any, Iterable, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from project.models import (
    AcademicTerm,
    AssessmentScheme,
    AssessmentSchemeComponent,
    ClassSection,
    Department,
    Grade,
    GradeStream,
    Section,
    Stream,
    Subject,
    SubjectOffering,
    Year,
)
from project.models.base.school_mixin import SchoolScopedMixin
from project.schema.blueprint_schema import BluePrintTemplate
from project.templates import TEM_DATA
from project.utils.enum import (
    AcademicTermEnum,
    AcademicTermTypeEnum,
    AcademicYearStatusEnum,
)

DEFAULT_BLUEPRINT_YEAR_NAME = "Default Academic Year Blueprint"
DEFAULT_BLUEPRINT_SCHEME_NAME = "Default Assessment Scheme"
DEFAULT_BLUEPRINT_SECTIONS = ("A", "B", "C")


class SchoolProvisioningError(RuntimeError):
    """Base error for school provisioning failures."""


class SchoolAlreadyProvisionedError(SchoolProvisioningError):
    """Raised when provisioning is attempted for a school that has tenant data."""


T = TypeVar("T", bound=SchoolScopedMixin)


@dataclass(slots=True)
class ProvisioningMaps:
    years: dict[uuid.UUID, uuid.UUID]
    terms: dict[uuid.UUID, uuid.UUID]
    subjects: dict[uuid.UUID, uuid.UUID]
    grades: dict[uuid.UUID, uuid.UUID]
    sections: dict[uuid.UUID, uuid.UUID]
    streams: dict[uuid.UUID, uuid.UUID]
    grade_streams: dict[uuid.UUID, uuid.UUID]
    assessment_schemes: dict[uuid.UUID, uuid.UUID]
    assessment_scheme_components: dict[uuid.UUID, uuid.UUID]
    subject_offerings: dict[uuid.UUID, uuid.UUID]
    class_sections: dict[uuid.UUID, uuid.UUID]

    @classmethod
    def empty(cls) -> "ProvisioningMaps":
        return cls(
            years={},
            terms={},
            subjects={},
            grades={},
            sections={},
            grade_streams={},
            streams={},
            assessment_schemes={},
            assessment_scheme_components={},
            subject_offerings={},
            class_sections={},
        )


class SchoolProvisioningService:
    """
    Copies global blueprint rows into tenant-owned school rows.

    Blueprint rows live in the same tables as tenant data and are identified by
    ``school_id IS NULL``. This service never commits; callers should run it in
    their existing transaction and commit or roll back once all school setup
    work succeeds.
    """

    @classmethod
    async def setup_school(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
    ) -> ProvisioningMaps:
        """
        Provision default academic setup for a new school.

        The method is intentionally fail-fast for idempotency: if tenant rows
        already exist in any provisioned table, it raises instead of creating
        partial duplicates.
        """

        await cls.ensure_default_blueprint(system_session=system_session)
        await cls._raise_if_school_has_provisioned_data(
            tenant_session=tenant_session,
            school_id=school_id,
        )
        return await cls._copy_blueprint(
            system_session=system_session,
            tenant_session=tenant_session,
            school_id=school_id,
        )

    @classmethod
    async def setup_academic_year_from_blueprint(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        year_id: uuid.UUID,
    ) -> ProvisioningMaps:
        """
        Copy blueprint academic setup into an existing tenant year.

        This replaces the legacy JSON default-year setup while preserving the
        existing year creation route. Tenant-level definitions such as subjects
        and grades are reused when they already exist for the school.
        """

        await cls.ensure_default_blueprint(system_session=system_session)
        maps = ProvisioningMaps.empty()

        blueprint_year_id = await cls._get_blueprint_year_id(system_session=system_session)
        if blueprint_year_id is None:
            raise ValueError("Blueprint year ID was not found")

        maps.years = {blueprint_year_id: year_id}

        await cls._ensure_terms(
            system_session=system_session,
            tenant_session=tenant_session,
            school_id=school_id,
            maps=maps,
        )
        await cls._ensure_subjects(
            system_session=system_session,
            tenant_session=tenant_session,
            school_id=school_id,
            maps=maps,
        )
        await cls._ensure_grades(
            system_session=system_session,
            tenant_session=tenant_session,
            school_id=school_id,
            maps=maps,
        )
        await cls._ensure_sections(
            system_session=system_session,
            tenant_session=tenant_session,
            school_id=school_id,
            maps=maps,
        )
        await cls._ensure_streams(
            system_session=system_session,
            tenant_session=tenant_session,
            school_id=school_id,
            maps=maps,
        )
        await cls._ensure_grade_streams(
            system_session=system_session,
            tenant_session=tenant_session,
            school_id=school_id,
            maps=maps,
        )
        await cls._copy_assessment_schemes(
            system_session=system_session,
            tenant_session=tenant_session,
            school_id=school_id,
            maps=maps,
            name_suffix=await cls._year_name(
                tenant_session=tenant_session,
                year_id=year_id,
            ),
        )
        await cls._copy_assessment_scheme_components(
            system_session=system_session,
            tenant_session=tenant_session,
            school_id=school_id,
            maps=maps,
        )
        await cls._copy_subject_offerings(
            system_session=system_session,
            tenant_session=tenant_session,
            school_id=school_id,
            maps=maps,
        )
        await cls._copy_class_sections(
            system_session=system_session,
            tenant_session=tenant_session,
            school_id=school_id,
            maps=maps,
        )
        return maps

    @classmethod
    async def setup_academic_year_from_payload(
        cls,
        *,
        tenant_session: AsyncSession,
        school_id: uuid.UUID,
        year_id: uuid.UUID,
        blueprint: BluePrintTemplate,
    ) -> None:
        """
        Setup academic year using a provided manual blueprint payload.
        """
        terms = (
            (await tenant_session.execute(select(AcademicTerm).where(AcademicTerm.year_id == year_id))).scalars().all()
        )

        if not terms:
            raise ValueError("Academic Terms must be created before setting up the payload.")

        # Create AssessmentScheme for this year
        year_name = await cls._year_name(tenant_session=tenant_session, year_id=year_id)
        scheme = AssessmentScheme(
            school_id=school_id,
            name=f"Manual Assessment Scheme - {year_name}",
            description="Generated scheme from manual setup",
        )
        tenant_session.add(scheme)
        await tenant_session.flush()

        # Create components
        components = []
        for idx, term in enumerate(terms):
            components.append(
                AssessmentSchemeComponent(
                    school_id=school_id,
                    term_id=term.id,
                    assessment_scheme_id=scheme.id,
                    description=f"Components for {term.name.value}",
                    name=f"{term.name.value} Continuous Assessment",
                    weight=40.0,
                    max_score=40.0,
                    display_order=1,
                )
            )
            components.append(
                AssessmentSchemeComponent(
                    school_id=school_id,
                    term_id=term.id,
                    assessment_scheme_id=scheme.id,
                    description=f"Components for {term.name.value}",
                    name=f"{term.name.value} Final Exam",
                    weight=60.0,
                    max_score=60.0,
                    display_order=2,
                )
            )
        tenant_session.add_all(components)
        await tenant_session.flush()

        # Process Subjects
        existing_subjects = (
            (await tenant_session.execute(select(Subject).where(Subject.school_id == school_id))).scalars().all()
        )
        subject_map = {s.code: s for s in existing_subjects}

        new_subjects = []
        for s_data in blueprint.subjects:
            if s_data.code not in subject_map:
                new_sub = Subject(school_id=school_id, name=s_data.name, code=s_data.code)
                new_subjects.append(new_sub)
                subject_map[s_data.code] = new_sub
        tenant_session.add_all(new_subjects)
        await tenant_session.flush()

        # Pre-fetch global Streams once outside the grade loop
        existing_streams = (
            (
                await tenant_session.execute(
                    select(Stream).where(
                        Stream.school_id == school_id,
                    )
                )
            )
            .scalars()
            .all()
        )
        stream_map = {s.name: s for s in existing_streams}

        # Pre-fetch existing SubjectOfferings for this year to prevent duplicates
        existing_offerings = (
            (
                await tenant_session.execute(
                    select(SubjectOffering).where(
                        SubjectOffering.school_id == school_id,
                        SubjectOffering.year_id == year_id,
                    )
                )
            )
            .scalars()
            .all()
        )
        offering_map = {(o.grade_stream_id, o.subject_id): o for o in existing_offerings}

        # Pre-fetch existing ClassSections for this year to prevent duplicates
        existing_class_sections = (
            (
                await tenant_session.execute(
                    select(ClassSection).where(
                        ClassSection.school_id == school_id,
                        ClassSection.academic_year_id == year_id,
                    )
                )
            )
            .scalars()
            .all()
        )
        class_section_map = {(cs.section_id, cs.grade_stream_id): cs for cs in existing_class_sections}

        # Process Grades, Sections, Streams, Offerings
        existing_grades = (
            (await tenant_session.execute(select(Grade).where(Grade.school_id == school_id))).scalars().all()
        )
        grade_map = {g.grade: g for g in existing_grades}

        for g_data in blueprint.grades:
            grade = grade_map.get(g_data.grade)
            if not grade:
                grade = Grade(
                    school_id=school_id,
                    grade=g_data.grade,
                    level=g_data.level,
                    has_stream=g_data.has_stream,
                )
                tenant_session.add(grade)
                await tenant_session.flush()
                grade_map[g_data.grade] = grade

            existing_grade_streams = (
                (
                    await tenant_session.execute(
                        select(GradeStream).where(
                            GradeStream.school_id == school_id,
                            GradeStream.grade_id == grade.id,
                        )
                    )
                )
                .scalars()
                .all()
            )
            grade_stream_map = {
                (grade_stream.grade_id, grade_stream.stream_id): grade_stream for grade_stream in existing_grade_streams
            }

            # Create Sections
            existing_sections = (
                (
                    await tenant_session.execute(
                        select(Section).where(Section.school_id == school_id, Section.grade_id == grade.id)
                    )
                )
                .scalars()
                .all()
            )
            section_map = {s.section: s for s in existing_sections}

            grade_sections = []
            for sec_data in blueprint.sections:
                section = section_map.get(sec_data.section)
                if not section:
                    section = Section(school_id=school_id, grade_id=grade.id, section=sec_data.section)
                    tenant_session.add(section)
                    section_map[sec_data.section] = section
                grade_sections.append(section)
            await tenant_session.flush()

            grade_streams: list[GradeStream] = []
            if g_data.has_stream and g_data.streams:
                for str_data in g_data.streams:
                    stream = stream_map.get(str_data.name)
                    if not stream:
                        stream = Stream(school_id=school_id, name=str_data.name)
                        tenant_session.add(stream)
                        stream_map[str_data.name] = stream

                    await tenant_session.flush()  # Flush after creating new Stream objects for IDs

                    grade_stream = grade_stream_map.get((grade.id, stream.id))
                    if not grade_stream:
                        grade_stream = GradeStream(school_id=school_id, grade_id=grade.id, stream_id=stream.id)
                        tenant_session.add(grade_stream)
                        grade_stream_map[(grade.id, stream.id)] = grade_stream
                    grade_streams.append(grade_stream)
                await tenant_session.flush()

                # Create Offerings for Streams
                for str_data, grade_stream in zip(g_data.streams, grade_streams):
                    for sub_data in str_data.subjects:
                        subject = subject_map[sub_data.code]
                        key = (grade_stream.id, subject.id)
                        if key not in offering_map:
                            offering = SubjectOffering(
                                school_id=school_id,
                                year_id=year_id,
                                subject_id=subject.id,
                                grade_stream_id=grade_stream.id,
                                assessment_scheme_id=scheme.id,
                            )
                            tenant_session.add(offering)
                            offering_map[key] = offering

            else:
                grade_stream = grade_stream_map.get((grade.id, None))
                if not grade_stream:
                    grade_stream = GradeStream(school_id=school_id, grade_id=grade.id, stream_id=None)
                    tenant_session.add(grade_stream)
                    grade_stream_map[(grade.id, None)] = grade_stream
                    await tenant_session.flush()
                grade_streams = [grade_stream]

                # Offerings for Grade without Streams
                for sub_data in g_data.subjects:
                    subject = subject_map[sub_data.code]
                    key = (grade_stream.id, subject.id)
                    if key not in offering_map:
                        offering = SubjectOffering(
                            school_id=school_id,
                            year_id=year_id,
                            subject_id=subject.id,
                            grade_stream_id=grade_stream.id,
                            assessment_scheme_id=scheme.id,
                        )
                        tenant_session.add(offering)
                        offering_map[key] = offering

            # ClassSections
            for i, section in enumerate(grade_sections):
                grade_stream = grade_streams[i % len(grade_streams)]
                cs_key = (section.id, grade_stream.id)
                if cs_key not in class_section_map:
                    cs = ClassSection(
                        school_id=school_id,
                        academic_year_id=year_id,
                        section_id=section.id,
                        grade_stream_id=grade_stream.id,
                    )
                    tenant_session.add(cs)
                    class_section_map[cs_key] = cs

            await tenant_session.flush()

    @classmethod
    async def setup_academic_year_from_previous_year(
        cls,
        *,
        tenant_session: AsyncSession,
        school_id: uuid.UUID,
        year_id: uuid.UUID,
    ) -> ProvisioningMaps:
        """
        Copy academic setup from the most recent previous year of the same school.
        """
        # Find the previous year
        previous_year = (
            await tenant_session.execute(
                select(Year)
                .where(Year.school_id == school_id, Year.id != year_id)
                .order_by(Year.created_at.desc())
                .limit(1)
            )
        ).scalar_one_or_none()

        if previous_year is None:
            raise ValueError("No previous academic year found to copy from.")

        maps = ProvisioningMaps.empty()
        maps.years = {previous_year.id: year_id}

        # 1. Copy terms
        previous_terms = (
            (await tenant_session.execute(select(AcademicTerm).where(AcademicTerm.year_id == previous_year.id)))
            .scalars()
            .all()
        )

        new_terms = []
        for term in previous_terms:
            new_term = AcademicTerm(
                school_id=school_id,
                year_id=year_id,
                name=term.name,
                start_date=term.start_date,
                end_date=term.end_date,
                registration_start=term.registration_start,
                registration_end=term.registration_end,
            )
            new_terms.append(new_term)
            tenant_session.add(new_term)
        await tenant_session.flush()

        # Update maps.terms after flush once client/database generates new_term IDs
        for old_term, new_term in zip(previous_terms, new_terms):
            maps.terms[old_term.id] = new_term.id

        # Reusing existing Subjects, Grades, Sections, Streams, and GradeStreams as they are school-scoped
        all_subjects = (
            (await tenant_session.execute(select(Subject).where(Subject.school_id == school_id))).scalars().all()
        )
        maps.subjects = {s.id: s.id for s in all_subjects}

        all_grades = (await tenant_session.execute(select(Grade).where(Grade.school_id == school_id))).scalars().all()
        maps.grades = {g.id: g.id for g in all_grades}

        all_sections = (
            (await tenant_session.execute(select(Section).where(Section.school_id == school_id))).scalars().all()
        )
        maps.sections = {s.id: s.id for s in all_sections}

        all_streams = (
            (await tenant_session.execute(select(Stream).where(Stream.school_id == school_id))).scalars().all()
        )
        maps.streams = {s.id: s.id for s in all_streams}

        all_grade_streams = (
            (await tenant_session.execute(select(GradeStream).where(GradeStream.school_id == school_id)))
            .scalars()
            .all()
        )
        maps.grade_streams = {gs.id: gs.id for gs in all_grade_streams}

        # Find assessment schemes used in the previous year
        previous_offerings = (
            (await tenant_session.execute(select(SubjectOffering).where(SubjectOffering.year_id == previous_year.id)))
            .scalars()
            .all()
        )

        scheme_ids = list(set(o.assessment_scheme_id for o in previous_offerings))

        current_year_name = await cls._year_name(tenant_session=tenant_session, year_id=year_id)

        if scheme_ids:
            previous_schemes = (
                (await tenant_session.execute(select(AssessmentScheme).where(AssessmentScheme.id.in_(scheme_ids))))
                .scalars()
                .all()
            )

            new_schemes = []
            for scheme in previous_schemes:
                # Remove old suffix if present, add new suffix
                base_name = scheme.name.split(" - ")[0]
                new_scheme = AssessmentScheme(
                    school_id=school_id,
                    name=f"{base_name} - {current_year_name}",
                    description=scheme.description,
                )
                new_schemes.append(new_scheme)
                tenant_session.add(new_scheme)
            await tenant_session.flush()

            for old_scheme, new_scheme in zip(previous_schemes, new_schemes):
                maps.assessment_schemes[old_scheme.id] = new_scheme.id

            # Copy components for these schemes
            previous_components = (
                (
                    await tenant_session.execute(
                        select(AssessmentSchemeComponent).where(
                            AssessmentSchemeComponent.assessment_scheme_id.in_(scheme_ids)
                        )
                    )
                )
                .scalars()
                .all()
            )

            new_components = []
            old_component_ids = []
            for component in previous_components:
                old_term = next((t for t in previous_terms if t.id == component.term_id), None)
                if old_term is None:
                    continue
                new_term = next((t for t in new_terms if t.name == old_term.name), None)
                if new_term is None:
                    continue

                new_component = AssessmentSchemeComponent(
                    school_id=school_id,
                    term_id=new_term.id,
                    assessment_scheme_id=maps.assessment_schemes[component.assessment_scheme_id],
                    name=component.name,
                    description=component.description,
                    weight=component.weight,
                    max_score=component.max_score,
                    display_order=component.display_order,
                )
                new_components.append(new_component)
                old_component_ids.append(component.id)
                tenant_session.add(new_component)
            await tenant_session.flush()

            for old_id, new_comp in zip(old_component_ids, new_components):
                maps.assessment_scheme_components[old_id] = new_comp.id

        # Deduplication map & creation for SubjectOfferings
        existing_target_offerings = (
            (await tenant_session.execute(select(SubjectOffering).where(SubjectOffering.year_id == year_id)))
            .scalars()
            .all()
        )
        existing_offering_keys = {(o.grade_stream_id, o.subject_id) for o in existing_target_offerings}

        new_offerings = []
        old_offering_ids = []
        for offering in previous_offerings:
            if offering.grade_stream_id not in maps.grade_streams:
                continue

            target_grade_stream_id = maps.grade_streams[offering.grade_stream_id]
            offering_key = (target_grade_stream_id, offering.subject_id)

            if offering_key not in existing_offering_keys:
                new_offering = SubjectOffering(
                    school_id=school_id,
                    year_id=year_id,
                    subject_id=offering.subject_id,
                    grade_stream_id=target_grade_stream_id,
                    assessment_scheme_id=maps.assessment_schemes.get(
                        offering.assessment_scheme_id, offering.assessment_scheme_id
                    ),
                )
                new_offerings.append(new_offering)
                old_offering_ids.append(offering.id)
                existing_offering_keys.add(offering_key)
                tenant_session.add(new_offering)

        if new_offerings:
            await tenant_session.flush()
            for old_id, new_off in zip(old_offering_ids, new_offerings):
                maps.subject_offerings[old_id] = new_off.id

        # Deduplication map & creation for ClassSections
        previous_class_sections = (
            (
                await tenant_session.execute(
                    select(ClassSection).where(ClassSection.academic_year_id == previous_year.id)
                )
            )
            .scalars()
            .all()
        )

        existing_target_class_sections = (
            (await tenant_session.execute(select(ClassSection).where(ClassSection.academic_year_id == year_id)))
            .scalars()
            .all()
        )
        existing_cs_keys = {(cs.section_id, cs.grade_stream_id) for cs in existing_target_class_sections}

        new_class_sections = []
        old_cs_ids = []
        for cs in previous_class_sections:
            if cs.grade_stream_id not in maps.grade_streams:
                continue

            target_grade_stream_id = maps.grade_streams[cs.grade_stream_id]
            cs_key = (cs.section_id, target_grade_stream_id)

            if cs_key not in existing_cs_keys:
                new_cs = ClassSection(
                    school_id=school_id,
                    section_id=cs.section_id,
                    grade_stream_id=target_grade_stream_id,
                    academic_year_id=year_id,
                    homeroom_teacher_id=None,
                )
                new_class_sections.append(new_cs)
                old_cs_ids.append(cs.id)
                existing_cs_keys.add(cs_key)
                tenant_session.add(new_cs)

        if new_class_sections:
            await tenant_session.flush()
            for old_id, new_cs in zip(old_cs_ids, new_class_sections):
                maps.class_sections[old_id] = new_cs.id

        return maps

    @classmethod
    async def ensure_default_blueprint(cls, *, system_session: AsyncSession) -> None:
        """Create the bundled global blueprint rows if no blueprint exists."""

        existing_year_id = await cls._get_blueprint_year_id(
            system_session=system_session,
            required=False,
        )
        if existing_year_id is not None:
            return

        template = BluePrintTemplate(**TEM_DATA)
        blueprint_year = Year(
            school_id=None,
            calendar_type=AcademicTermTypeEnum.SEMESTER,
            name=DEFAULT_BLUEPRINT_YEAR_NAME,
            start_date=date(2026, 9, 1),
            end_date=date(2027, 6, 30),
            status=AcademicYearStatusEnum.UPCOMING,
        )
        system_session.add(blueprint_year)
        await system_session.flush()

        terms: list[AcademicTerm] = []
        for index, term_name in enumerate((AcademicTermEnum.FIRST_TERM, AcademicTermEnum.SECOND_TERM), start=1):
            term = AcademicTerm(
                school_id=None,
                year_id=blueprint_year.id,
                name=term_name,
                start_date=date(2026 if index == 1 else 2027, 9 if index == 1 else 2, 1),
                end_date=date(2027, 1 if index == 1 else 6, 31 if index == 1 else 30),
                registration_start=None,
                registration_end=None,
            )
            terms.append(term)
        system_session.add_all(terms)
        await system_session.flush()

        scheme = AssessmentScheme(
            school_id=None,
            name=DEFAULT_BLUEPRINT_SCHEME_NAME,
            description="Default continuous assessment and final exam weighting.",
        )
        system_session.add(scheme)
        await system_session.flush()

        components: list[AssessmentSchemeComponent] = []
        for term in terms:
            components.extend(
                [
                    AssessmentSchemeComponent(
                        school_id=None,
                        term_id=term.id,
                        assessment_scheme_id=scheme.id,
                        name=f"Term {term.name.value} Continuous Assessment",
                        description="Classwork, quizzes, assignments, and projects.",
                        weight=40.0,
                        max_score=40.0,
                        display_order=1,
                    ),
                    AssessmentSchemeComponent(
                        school_id=None,
                        term_id=term.id,
                        assessment_scheme_id=scheme.id,
                        name=f"Term {term.name.value} Final Exam",
                        description="End of term examination.",
                        weight=60.0,
                        max_score=60.0,
                        display_order=2,
                    ),
                ]
            )
        system_session.add_all(components)

        subjects = [
            Subject(
                school_id=None,
                name=subject.name,
                code=subject.code,
            )
            for subject in template.subjects
        ]
        system_session.add_all(subjects)
        await system_session.flush()
        subject_by_name = {subject.name: subject for subject in subjects}

        # Track global streams across grades to prevent duplicates
        global_stream_map: dict[str, Stream] = {}

        grade_by_value: dict[uuid.UUID, Grade] = {}
        sections_by_grade: dict[uuid.UUID, list[Section]] = {}
        grade_streams_by_grade: dict[uuid.UUID, list[GradeStream]] = {}

        offerings: list[SubjectOffering] = []
        class_sections: list[ClassSection] = []

        for grade_data in template.grades:
            grade = Grade(
                school_id=None,
                grade=grade_data.grade,
                level=grade_data.level,
                has_stream=grade_data.has_stream,
            )
            system_session.add(grade)
            await system_session.flush()
            grade_by_value[grade.id] = grade

            # Collect sections for this grade
            grade_sections = [
                Section(
                    school_id=None,
                    grade_id=grade.id,
                    section=section_name,
                )
                for section_name in DEFAULT_BLUEPRINT_SECTIONS
            ]
            system_session.add_all(grade_sections)
            sections_by_grade[grade.id] = grade_sections

            current_grade_streams: list[GradeStream] = []

            if grade_data.streams:
                for stream_data in grade_data.streams:
                    stream = global_stream_map.get(stream_data.name)
                    if not stream:
                        stream = Stream(
                            school_id=None,
                            name=stream_data.name,
                        )
                        system_session.add(stream)
                        await system_session.flush()
                        global_stream_map[stream_data.name] = stream

                    grade_stream = GradeStream(
                        school_id=None,
                        grade_id=grade.id,
                        stream_id=stream.id,
                    )
                    system_session.add(grade_stream)
                    await system_session.flush()
                    current_grade_streams.append(grade_stream)

                    for subject_data in stream_data.subjects:
                        offerings.append(
                            SubjectOffering(
                                school_id=None,
                                year_id=blueprint_year.id,
                                subject_id=subject_by_name[subject_data.name].id,
                                grade_stream_id=grade_stream.id,
                                assessment_scheme_id=scheme.id,
                            )
                        )
            else:
                grade_stream = GradeStream(
                    school_id=None,
                    grade_id=grade.id,
                    stream_id=None,
                )
                system_session.add(grade_stream)
                await system_session.flush()
                current_grade_streams.append(grade_stream)

                for subject_data in grade_data.subjects:
                    offerings.append(
                        SubjectOffering(
                            school_id=None,
                            year_id=blueprint_year.id,
                            subject_id=subject_by_name[subject_data.name].id,
                            grade_stream_id=grade_stream.id,
                            assessment_scheme_id=scheme.id,
                        )
                    )

            grade_streams_by_grade[grade.id] = current_grade_streams

            # Create ClassSections per grade using local section indices
            for local_idx, section in enumerate(grade_sections):
                assigned_stream = current_grade_streams[local_idx % len(current_grade_streams)]
                class_sections.append(
                    ClassSection(
                        school_id=None,
                        section_id=section.id,
                        grade_stream_id=assigned_stream.id,
                        academic_year_id=blueprint_year.id,
                    )
                )

        system_session.add_all(offerings)
        system_session.add_all(class_sections)

        department = Department(
            school_id=None,
            name="Teaching",
            code="TEACH",
            head_employee_id=None,
        )

        system_session.add(department)
        await system_session.flush()

    @classmethod
    async def _copy_blueprint(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
    ) -> ProvisioningMaps:
        maps = ProvisioningMaps.empty()

        await cls._copy_years(
            system_session=system_session,
            tenant_session=tenant_session,
            school_id=school_id,
            maps=maps,
        )
        await cls._copy_terms(
            system_session=system_session,
            tenant_session=tenant_session,
            school_id=school_id,
            maps=maps,
        )
        await cls._copy_subjects(
            system_session=system_session,
            tenant_session=tenant_session,
            school_id=school_id,
            maps=maps,
        )
        await cls._copy_grades(
            system_session=system_session,
            tenant_session=tenant_session,
            school_id=school_id,
            maps=maps,
        )
        await cls._copy_sections(
            system_session=system_session,
            tenant_session=tenant_session,
            school_id=school_id,
            maps=maps,
        )
        await cls._copy_streams(
            system_session=system_session,
            tenant_session=tenant_session,
            school_id=school_id,
            maps=maps,
        )
        await cls._copy_grade_streams(
            system_session=system_session,
            tenant_session=tenant_session,
            school_id=school_id,
            maps=maps,
        )
        await cls._copy_assessment_schemes(
            system_session=system_session,
            tenant_session=tenant_session,
            school_id=school_id,
            maps=maps,
        )
        await cls._copy_assessment_scheme_components(
            system_session=system_session,
            tenant_session=tenant_session,
            school_id=school_id,
            maps=maps,
        )
        await cls._copy_subject_offerings(
            system_session=system_session,
            tenant_session=tenant_session,
            school_id=school_id,
            maps=maps,
        )
        await cls._copy_class_sections(
            system_session=system_session,
            tenant_session=tenant_session,
            school_id=school_id,
            maps=maps,
        )
        return maps

    @staticmethod
    async def _raise_if_school_has_provisioned_data(
        *,
        tenant_session: AsyncSession,
        school_id: uuid.UUID,
    ) -> None:
        checks = (
            Year,
            Subject,
            Grade,
            Section,
            Stream,
            AssessmentScheme,
            AssessmentSchemeComponent,
            SubjectOffering,
            ClassSection,
        )
        for model in checks:
            count = (
                await tenant_session.execute(
                    select(func.count()).select_from(model).where(model.school_id == school_id)
                )
            ).scalar_one()
            if count:
                raise SchoolAlreadyProvisionedError(f"School {school_id} already has {model.__tablename__} rows.")

    @staticmethod
    async def _get_blueprint_year_id(
        *,
        system_session: AsyncSession,
        required: bool = True,
    ) -> uuid.UUID | None:
        blueprint_year = (
            await system_session.execute(
                select(Year).where(
                    Year.school_id.is_(None),
                    Year.name == DEFAULT_BLUEPRINT_YEAR_NAME,
                ),
                execution_options={"skip_school_scope": True},
            )
        ).scalar_one_or_none()
        if blueprint_year is None and required:
            raise SchoolProvisioningError("Default tenant blueprint year was not found.")
        return blueprint_year.id if blueprint_year is not None else None

    @staticmethod
    async def _year_name(*, tenant_session: AsyncSession, year_id: uuid.UUID) -> str:
        year = (await tenant_session.execute(select(Year).where(Year.id == year_id))).scalar_one_or_none()
        if year is None:
            raise SchoolProvisioningError(f"Year {year_id} was not found.")
        return year.name

    @staticmethod
    async def _blueprint_rows(
        *,
        system_session: AsyncSession,
        model: type[T],
    ) -> list[T]:
        result = await system_session.execute(
            select(model).where(model.school_id.is_(None)),
            execution_options={"skip_school_scope": True},
        )
        return list(result.scalars().all())

    @staticmethod
    async def _tenant_rows_by_key(
        tenant_session: AsyncSession,
        model: type[T],
        school_id: uuid.UUID,
        rows: Iterable[Any],
        key_fields: tuple[str, ...],
    ) -> dict[tuple[Any, ...], T]:
        rows_list = list(rows)
        if not rows_list:
            return {}

        # Pre-compute blueprint key set once O(N)
        target_keys = {tuple(getattr(source, field) for field in key_fields) for source in rows_list}

        # Handle composite vs single key filtering
        if len(key_fields) == 1:
            field_name = key_fields[0]
            field_attr = getattr(model, field_name)
            distinct_values = {k[0] for k in target_keys}

            stmt = select(model).where(
                model.school_id == school_id,
                field_attr.in_(distinct_values),
            )
        else:
            # Fallback to fetching tenant rows and matching against pre-computed keys
            stmt = select(model).where(model.school_id == school_id)

        tenant_rows = (await tenant_session.execute(stmt)).scalars().all()

        result: dict[tuple[Any, ...], T] = {}
        for row in tenant_rows:
            row_key = tuple(getattr(row, field) for field in key_fields)
            if row_key in target_keys:
                result[row_key] = row

        return result

    @classmethod
    async def _copy_years(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        years = await cls._blueprint_rows(
            system_session=system_session,
            model=Year,
        )
        if not years:
            return

        # Fetch existing target years to prevent duplicate insertions
        existing_target_years = (
            (await tenant_session.execute(select(Year).where(Year.school_id == school_id))).scalars().all()
        )
        existing_year_names = {y.name for y in existing_target_years}

        new_rows: list[Year] = []
        blueprint_year_ids: list[uuid.UUID] = []

        for year in years:
            clean_name = year.name.replace(" Blueprint", "")
            if clean_name not in existing_year_names:
                new_year = Year(
                    school_id=school_id,
                    calendar_type=year.calendar_type,
                    name=clean_name,
                    start_date=year.start_date,
                    end_date=year.end_date,
                    status=year.status,
                )
                new_rows.append(new_year)
                blueprint_year_ids.append(year.id)
                existing_year_names.add(clean_name)

            tenant_session.add_all(new_rows)
            await tenant_session.flush()

            # Safely populate ProvisioningMaps post-flush after Primary Keys exist
            for blueprint_id, new_yr in zip(blueprint_year_ids, new_rows):
                maps.years[blueprint_id] = new_yr.id

    @classmethod
    async def _copy_terms(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        terms = await cls._blueprint_rows(
            system_session=system_session,
            model=AcademicTerm,
        )
        if not terms or not maps.years:
            return

        # Query existing target terms for the provisioned target years
        target_year_ids = list(set(maps.years.values()))
        existing_target_terms = (
            (
                await tenant_session.execute(
                    select(AcademicTerm).where(
                        AcademicTerm.school_id == school_id,
                        AcademicTerm.year_id.in_(target_year_ids),
                    )
                )
            )
            .scalars()
            .all()
        )
        existing_term_keys = {(t.year_id, t.name) for t in existing_target_terms}

        new_rows: list[AcademicTerm] = []
        blueprint_term_ids: list[uuid.UUID] = []

        for term in terms:
            if term.year_id not in maps.years:
                continue

            target_year_id = maps.years[term.year_id]
            term_key = (target_year_id, term.name)

            if term_key not in existing_term_keys:
                new_term = AcademicTerm(
                    school_id=school_id,
                    year_id=target_year_id,
                    name=term.name,
                    start_date=term.start_date,
                    end_date=term.end_date,
                    registration_start=term.registration_start,
                    registration_end=term.registration_end,
                )
                new_rows.append(new_term)
                blueprint_term_ids.append(term.id)
                existing_term_keys.add(term_key)

            tenant_session.add_all(new_rows)
            await tenant_session.flush()

            # Safely populate ProvisioningMaps post-flush
            for blueprint_id, new_trm in zip(blueprint_term_ids, new_rows):
                maps.terms[blueprint_id] = new_trm.id

    @classmethod
    async def _ensure_terms(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        terms = await cls._blueprint_rows(
            system_session=system_session,
            model=AcademicTerm,
        )
        tenant_year_ids = set(maps.years.values())
        if not terms or not tenant_year_ids:
            return

        tenant_terms = (
            (
                await tenant_session.execute(
                    select(AcademicTerm).where(
                        AcademicTerm.school_id == school_id,
                        AcademicTerm.year_id.in_(tenant_year_ids),
                    )
                )
            )
            .scalars()
            .all()
        )
        existing = {(term.year_id, term.name): term for term in tenant_terms}

        new_rows: list[AcademicTerm] = []
        pending_mappings: list[tuple[uuid.UUID, AcademicTerm]] = []

        for term in terms:
            tenant_year_id = maps.years.get(term.year_id)
            if tenant_year_id is None:
                continue

            cache_key = (tenant_year_id, term.name)
            tenant_term = existing.get(cache_key)

            if tenant_term is None:
                tenant_term = AcademicTerm(
                    school_id=school_id,
                    year_id=tenant_year_id,
                    name=term.name,
                    start_date=term.start_date,
                    end_date=term.end_date,
                    registration_start=term.registration_start,
                    registration_end=term.registration_end,
                )
                new_rows.append(tenant_term)
                existing[cache_key] = tenant_term
                pending_mappings.append((term.id, tenant_term))
            else:
                maps.terms[term.id] = tenant_term.id

            tenant_session.add_all(new_rows)
            await tenant_session.flush()

            # Safely map newly generated Primary Keys post-flush
            for blueprint_id, new_trm in pending_mappings:
                maps.terms[blueprint_id] = new_trm.id

    @classmethod
    async def _copy_subjects(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        subjects = await cls._blueprint_rows(
            system_session=system_session,
            model=Subject,
        )
        if not subjects:
            return

        # Fetch existing target subjects to prevent duplicates
        existing_target_subjects = (
            (await tenant_session.execute(select(Subject).where(Subject.school_id == school_id))).scalars().all()
        )
        existing_subject_codes = {s.code for s in existing_target_subjects}

        new_rows: list[Subject] = []
        blueprint_subject_ids: list[uuid.UUID] = []

        for subject in subjects:
            if subject.code not in existing_subject_codes:
                new_subject = Subject(
                    school_id=school_id,
                    name=subject.name,
                    code=subject.code,
                )
                new_rows.append(new_subject)
                blueprint_subject_ids.append(subject.id)
                existing_subject_codes.add(subject.code)

            tenant_session.add_all(new_rows)
            await tenant_session.flush()

            # Safely update ProvisioningMaps post-flush after Primary Keys are assigned
            for blueprint_id, new_sub in zip(blueprint_subject_ids, new_rows):
                maps.subjects[blueprint_id] = new_sub.id

    @classmethod
    async def _ensure_subjects(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        subjects = await cls._blueprint_rows(
            system_session=system_session,
            model=Subject,
        )
        if not subjects:
            return

        existing = await cls._tenant_rows_by_key(
            tenant_session,
            Subject,
            school_id,
            subjects,
            ("code",),
        )
        new_rows: list[Subject] = []
        pending_mappings: list[tuple[uuid.UUID, Subject]] = []

        for subject in subjects:
            cache_key = (subject.code,)
            tenant_subject = existing.get(cache_key)

            if tenant_subject is None:
                tenant_subject = Subject(
                    school_id=school_id,
                    name=subject.name,
                    code=subject.code,
                )
                new_rows.append(tenant_subject)
                existing[cache_key] = tenant_subject
                pending_mappings.append((subject.id, tenant_subject))
            else:
                maps.subjects[subject.id] = tenant_subject.id

            tenant_session.add_all(new_rows)
            await tenant_session.flush()

            # Safely map blueprint IDs to generated primary keys after flush
            for blueprint_id, new_sub in pending_mappings:
                maps.subjects[blueprint_id] = new_sub.id

    @classmethod
    async def _copy_grades(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        grades = await cls._blueprint_rows(
            system_session=system_session,
            model=Grade,
        )
        if not grades:
            return

        # Fetch existing target grades to avoid duplicates on re-provisioning
        existing_target_grades = (
            (await tenant_session.execute(select(Grade).where(Grade.school_id == school_id))).scalars().all()
        )
        existing_grade_names = {g.grade for g in existing_target_grades}

        new_rows: list[Grade] = []
        blueprint_grade_ids: list[uuid.UUID] = []

        for grade in grades:
            if grade.grade not in existing_grade_names:
                new_grade = Grade(
                    school_id=school_id,
                    grade=grade.grade,
                    level=grade.level,
                    has_stream=grade.has_stream,
                )
                new_rows.append(new_grade)
                blueprint_grade_ids.append(grade.id)
                existing_grade_names.add(grade.grade)

            tenant_session.add_all(new_rows)
            await tenant_session.flush()

            # Safely update ProvisioningMaps post-flush
            for blueprint_id, new_grd in zip(blueprint_grade_ids, new_rows):
                maps.grades[blueprint_id] = new_grd.id

    @classmethod
    async def _ensure_grades(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        grades = await cls._blueprint_rows(
            system_session=system_session,
            model=Grade,
        )
        if not grades:
            return

        tenant_grades = (
            (await tenant_session.execute(select(Grade).where(Grade.school_id == school_id))).scalars().all()
        )
        existing = {grade.grade: grade for grade in tenant_grades}

        new_rows: list[Grade] = []
        pending_mappings: list[tuple[uuid.UUID, Grade]] = []

        for grade in grades:
            tenant_grade = existing.get(grade.grade)

            if tenant_grade is None:
                tenant_grade = Grade(
                    school_id=school_id,
                    grade=grade.grade,
                    level=grade.level,
                    has_stream=grade.has_stream,
                )
                new_rows.append(tenant_grade)
                existing[grade.grade] = tenant_grade
                pending_mappings.append((grade.id, tenant_grade))
            else:
                maps.grades[grade.id] = tenant_grade.id

            tenant_session.add_all(new_rows)
            await tenant_session.flush()

            # Safely update ProvisioningMaps post-flush after Primary Keys are assigned
            for blueprint_id, new_grd in pending_mappings:
                maps.grades[blueprint_id] = new_grd.id

    @classmethod
    async def _copy_sections(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        sections = await cls._blueprint_rows(
            system_session=system_session,
            model=Section,
        )
        if not sections:
            return

        # Fetch existing target sections to prevent duplicates
        target_grade_ids = list(set(maps.grades.values()))
        existing_target_sections = (
            (
                await tenant_session.execute(
                    select(Section).where(
                        Section.school_id == school_id,
                        Section.grade_id.in_(target_grade_ids),
                    )
                )
            )
            .scalars()
            .all()
        )
        existing_section_keys = {(s.grade_id, s.section) for s in existing_target_sections}

        new_rows: list[Section] = []
        blueprint_section_ids: list[uuid.UUID] = []

        for section in sections:
            if section.grade_id not in maps.grades:
                continue

            target_grade_id = maps.grades[section.grade_id]
            section_key = (target_grade_id, section.section)

            if section_key not in existing_section_keys:
                new_section = Section(
                    school_id=school_id,
                    grade_id=target_grade_id,
                    section=section.section,
                )
                new_rows.append(new_section)
                blueprint_section_ids.append(section.id)
                existing_section_keys.add(section_key)

            tenant_session.add_all(new_rows)
            await tenant_session.flush()

            for blueprint_id, new_sec in zip(blueprint_section_ids, new_rows):
                maps.sections[blueprint_id] = new_sec.id

    @classmethod
    async def _ensure_sections(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        sections = await cls._blueprint_rows(
            system_session=system_session,
            model=Section,
        )
        if not sections:
            return

        tenant_sections = (
            (await tenant_session.execute(select(Section).where(Section.school_id == school_id))).scalars().all()
        )
        existing = {(section.grade_id, section.section): section for section in tenant_sections}

        new_rows: list[Section] = []
        pending_mappings: list[tuple[uuid.UUID, Section]] = []

        for section in sections:
            tenant_grade_id = maps.grades.get(section.grade_id)
            if tenant_grade_id is None:
                continue

            cache_key = (tenant_grade_id, section.section)
            tenant_section = existing.get(cache_key)

            if tenant_section is None:
                tenant_section = Section(
                    school_id=school_id,
                    grade_id=tenant_grade_id,
                    section=section.section,
                )
                new_rows.append(tenant_section)
                existing[cache_key] = tenant_section
                pending_mappings.append((section.id, tenant_section))
            else:
                maps.sections[section.id] = tenant_section.id

            tenant_session.add_all(new_rows)
            await tenant_session.flush()

            # Safely map newly generated Primary Keys post-flush
            for blueprint_id, new_sec in pending_mappings:
                maps.sections[blueprint_id] = new_sec.id

    @classmethod
    async def _copy_streams(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        streams = await cls._blueprint_rows(
            system_session=system_session,
            model=Stream,
        )
        if not streams:
            return

        # Fetch existing target streams to prevent duplicates
        existing_target_streams = (
            (
                await tenant_session.execute(
                    select(Stream).where(
                        Stream.school_id == school_id,
                    )
                )
            )
            .scalars()
            .all()
        )
        existing_stream_names = {s.name for s in existing_target_streams}

        new_rows: list[Stream] = []
        blueprint_stream_ids: list[uuid.UUID] = []

        for stream in streams:
            if stream.name not in existing_stream_names:
                new_stream = Stream(
                    school_id=school_id,
                    name=stream.name,
                )
                new_rows.append(new_stream)
                blueprint_stream_ids.append(stream.id)
                existing_stream_names.add(stream.name)

            tenant_session.add_all(new_rows)
            await tenant_session.flush()

            for blueprint_id, new_st in zip(blueprint_stream_ids, new_rows):
                maps.streams[blueprint_id] = new_st.id

    @classmethod
    async def _ensure_streams(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        streams = await cls._blueprint_rows(system_session=system_session, model=Stream)
        tenant_streams = (
            (await tenant_session.execute(select(Stream).where(Stream.school_id == school_id))).scalars().all()
        )
        existing_streams = {stream.name: stream for stream in tenant_streams}

        new_streams: list[Stream] = []

        for stream in streams:
            tenant_stream = existing_streams.get(stream.name)
            if tenant_stream is None:
                tenant_stream = Stream(
                    school_id=school_id,
                    name=stream.name,
                )
                new_streams.append(tenant_stream)
                existing_streams[stream.name] = tenant_stream

        tenant_session.add_all(new_streams)
        await tenant_session.flush()

        # Populate the maps.streams dictionary once IDs are generated
        for stream in streams:
            tenant_stream = existing_streams.get(stream.name)
            if tenant_stream:
                maps.streams[stream.id] = tenant_stream.id

    @classmethod
    async def _ensure_grade_streams(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        system_grade_streams = await cls._blueprint_rows(
            system_session=system_session,
            model=GradeStream,
        )
        if not system_grade_streams:
            return

        tenant_links = (
            (await tenant_session.execute(select(GradeStream).where(GradeStream.school_id == school_id)))
            .scalars()
            .all()
        )
        # Store actual instances in the map so we can access link.id for existing rows
        existing_links = {(link.grade_id, link.stream_id): link for link in tenant_links}

        new_links: list[GradeStream] = []
        pending_mappings: list[tuple[uuid.UUID, GradeStream]] = []

        for gs in system_grade_streams:
            tenant_grade_id = maps.grades.get(gs.grade_id)
            tenant_stream_id = maps.streams.get(gs.stream_id) if gs.stream_id is not None else None

            if tenant_grade_id is None:
                continue

            cache_key = (tenant_grade_id, tenant_stream_id)
            tenant_link = existing_links.get(cache_key)

            if tenant_link is None:
                tenant_link = GradeStream(
                    school_id=school_id,
                    grade_id=tenant_grade_id,
                    stream_id=tenant_stream_id,
                )
                new_links.append(tenant_link)
                existing_links[cache_key] = tenant_link
                pending_mappings.append((gs.id, tenant_link))
            else:
                maps.grade_streams[gs.id] = tenant_link.id

            tenant_session.add_all(new_links)
            await tenant_session.flush()

            for blueprint_id, new_link in pending_mappings:
                maps.grade_streams[blueprint_id] = new_link.id

    @classmethod
    async def _copy_grade_streams(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        grade_streams = await cls._blueprint_rows(
            system_session=system_session,
            model=GradeStream,
        )
        if not grade_streams:
            return

        # Fetch existing target grade streams to prevent duplicate insertions
        target_grade_ids = list(set(maps.grades.values()))
        existing_target_gs = (
            (
                await tenant_session.execute(
                    select(GradeStream).where(
                        GradeStream.school_id == school_id,
                        GradeStream.grade_id.in_(target_grade_ids),
                    )
                )
            )
            .scalars()
            .all()
        )
        existing_gs_keys = {(gs.grade_id, gs.stream_id) for gs in existing_target_gs}

        new_rows: list[GradeStream] = []
        blueprint_gs_ids: list[uuid.UUID] = []

        for gs in grade_streams:
            if gs.grade_id not in maps.grades or (gs.stream_id not in maps.streams and gs.stream_id is not None):
                continue

            target_grade_id = maps.grades[gs.grade_id]
            target_stream_id = maps.streams[gs.stream_id] if gs.stream_id is not None else None
            gs_key = (target_grade_id, target_stream_id)

            if gs_key not in existing_gs_keys:
                new_gs = GradeStream(
                    school_id=school_id,
                    grade_id=target_grade_id,
                    stream_id=target_stream_id,
                )
                new_rows.append(new_gs)
                blueprint_gs_ids.append(gs.id)
                existing_gs_keys.add(gs_key)

            tenant_session.add_all(new_rows)
            await tenant_session.flush()

            for blueprint_id, new_gs in zip(blueprint_gs_ids, new_rows):
                maps.grade_streams[blueprint_id] = new_gs.id

    @classmethod
    async def _copy_assessment_schemes(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
        name_suffix: str | None = None,
    ) -> None:
        schemes = await cls._blueprint_rows(
            system_session=system_session,
            model=AssessmentScheme,
        )
        if not schemes:
            return

        # Fetch existing target assessment schemes to prevent duplicates
        existing_target_schemes = (
            (
                await tenant_session.execute(
                    select(AssessmentScheme).where(
                        AssessmentScheme.school_id == school_id,
                    )
                )
            )
            .scalars()
            .all()
        )
        existing_scheme_names = {s.name for s in existing_target_schemes}

        new_rows: list[AssessmentScheme] = []
        blueprint_scheme_ids: list[uuid.UUID] = []

        for scheme in schemes:
            name = scheme.name if name_suffix is None else f"{scheme.name} - {name_suffix}"

            if name not in existing_scheme_names:
                new_scheme = AssessmentScheme(
                    school_id=school_id,
                    name=name,
                    description=scheme.description,
                )
                new_rows.append(new_scheme)
                blueprint_scheme_ids.append(scheme.id)
                existing_scheme_names.add(name)

            tenant_session.add_all(new_rows)
            await tenant_session.flush()

            for blueprint_id, new_sch in zip(blueprint_scheme_ids, new_rows):
                maps.assessment_schemes[blueprint_id] = new_sch.id

    @classmethod
    async def _copy_assessment_scheme_components(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        components = await cls._blueprint_rows(
            system_session=system_session,
            model=AssessmentSchemeComponent,
        )
        if not components:
            return

        # Fetch existing target components to prevent duplicates
        target_scheme_ids = list(set(maps.assessment_schemes.values()))
        existing_target_components = (
            (
                await tenant_session.execute(
                    select(AssessmentSchemeComponent).where(
                        AssessmentSchemeComponent.school_id == school_id,
                        AssessmentSchemeComponent.assessment_scheme_id.in_(target_scheme_ids),
                    )
                )
            )
            .scalars()
            .all()
        )
        existing_component_keys = {(c.assessment_scheme_id, c.term_id, c.name) for c in existing_target_components}

        new_rows: list[AssessmentSchemeComponent] = []
        blueprint_component_ids: list[uuid.UUID] = []

        for component in components:
            if component.term_id not in maps.terms or component.assessment_scheme_id not in maps.assessment_schemes:
                continue

            target_term_id = maps.terms[component.term_id]
            target_scheme_id = maps.assessment_schemes[component.assessment_scheme_id]
            component_key = (target_scheme_id, target_term_id, component.name)

            if component_key not in existing_component_keys:
                new_component = AssessmentSchemeComponent(
                    school_id=school_id,
                    term_id=target_term_id,
                    assessment_scheme_id=target_scheme_id,
                    name=component.name,
                    description=component.description,
                    weight=component.weight,
                    max_score=component.max_score,
                    display_order=component.display_order,
                )
                new_rows.append(new_component)
                blueprint_component_ids.append(component.id)
                existing_component_keys.add(component_key)

            tenant_session.add_all(new_rows)
            await tenant_session.flush()

            # Safely update ProvisioningMaps after flush guarantees populated Primary Keys
            for blueprint_id, new_comp in zip(blueprint_component_ids, new_rows):
                maps.assessment_scheme_components[blueprint_id] = new_comp.id

    @classmethod
    async def _copy_subject_offerings(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        offerings = await cls._blueprint_rows(
            system_session=system_session,
            model=SubjectOffering,
        )
        if not offerings:
            return

        # Fetch existing target offerings to prevent duplicate inserts
        target_year_ids = set(maps.years.values())
        existing_target_offerings = (
            (
                await tenant_session.execute(
                    select(SubjectOffering).where(
                        SubjectOffering.school_id == school_id,
                        SubjectOffering.year_id.in_(target_year_ids),
                    )
                )
            )
            .scalars()
            .all()
        )
        existing_offering_keys = {(o.year_id, o.grade_stream_id, o.subject_id) for o in existing_target_offerings}

        new_rows: list[SubjectOffering] = []
        blueprint_offering_ids: list[uuid.UUID] = []

        for offering in offerings:
            if (
                offering.year_id not in maps.years
                or offering.subject_id not in maps.subjects
                or offering.grade_stream_id not in maps.grade_streams
                or offering.assessment_scheme_id not in maps.assessment_schemes
            ):
                continue

            target_year_id = maps.years[offering.year_id]
            target_subject_id = maps.subjects[offering.subject_id]
            target_grade_stream_id = maps.grade_streams[offering.grade_stream_id]
            target_scheme_id = maps.assessment_schemes[offering.assessment_scheme_id]

            offering_key = (target_year_id, target_grade_stream_id, target_subject_id)

            if offering_key not in existing_offering_keys:
                new_offering = SubjectOffering(
                    school_id=school_id,
                    year_id=target_year_id,
                    subject_id=target_subject_id,
                    grade_stream_id=target_grade_stream_id,
                    assessment_scheme_id=target_scheme_id,
                )
                new_rows.append(new_offering)
                blueprint_offering_ids.append(offering.id)
                existing_offering_keys.add(offering_key)

            tenant_session.add_all(new_rows)
            await tenant_session.flush()

            # Safely populate maps after flush guarantees populated Primary Keys
            for blueprint_id, new_offering in zip(blueprint_offering_ids, new_rows):
                maps.subject_offerings[blueprint_id] = new_offering.id

    @classmethod
    async def _copy_class_sections(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        class_sections = await cls._blueprint_rows(
            system_session=system_session,
            model=ClassSection,
        )
        if not class_sections:
            return

        # Fetch existing target class sections to prevent duplicates
        target_year_ids = set(maps.years.values())
        existing_target_cs = (
            (
                await tenant_session.execute(
                    select(ClassSection).where(
                        ClassSection.school_id == school_id,
                        ClassSection.academic_year_id.in_(target_year_ids),
                    )
                )
            )
            .scalars()
            .all()
        )
        existing_cs_keys = {(cs.academic_year_id, cs.section_id, cs.grade_stream_id) for cs in existing_target_cs}

        new_rows: list[ClassSection] = []
        blueprint_cs_ids: list[uuid.UUID] = []

        for class_section in class_sections:
            if (
                class_section.section_id not in maps.sections
                or class_section.academic_year_id not in maps.years
                or class_section.grade_stream_id not in maps.grade_streams
            ):
                continue

            target_year_id = maps.years[class_section.academic_year_id]
            target_section_id = maps.sections[class_section.section_id]
            target_grade_stream_id = maps.grade_streams[class_section.grade_stream_id]

            cs_key = (target_year_id, target_section_id, target_grade_stream_id)

            if cs_key not in existing_cs_keys:
                new_class_section = ClassSection(
                    school_id=school_id,
                    section_id=target_section_id,
                    grade_stream_id=target_grade_stream_id,
                    academic_year_id=target_year_id,
                    homeroom_teacher_id=None,
                )
                new_rows.append(new_class_section)
                blueprint_cs_ids.append(class_section.id)
                existing_cs_keys.add(cs_key)

            tenant_session.add_all(new_rows)
            await tenant_session.flush()

            # Map old IDs to generated target IDs after flush
            for blueprint_id, new_cs in zip(blueprint_cs_ids, new_rows):
                maps.class_sections[blueprint_id] = new_cs.id
