"""Tenant blueprint provisioning service."""

import uuid
from dataclasses import dataclass
from datetime import date
from typing import Iterable, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from project.models import (
    AcademicTerm,
    AssessmentScheme,
    AssessmentSchemeComponent,
    ClassSection,
    Department,
    Grade,
    School,
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
        # Since this is manual setup, Year is already created.
        # Academic Terms are already created during Year creation.
        # AssessmentScheme could be created dynamically or just use default ones for now
        # but let's assume terms are there.
        # We fetch them to create default AssessmentScheme.

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
            else:
                # Update existing grade flags if necessary
                grade.has_stream = g_data.has_stream

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

            grade_streams = []
            if g_data.has_stream and g_data.streams:
                existing_streams = (
                    (
                        await tenant_session.execute(
                            select(Stream).where(
                                Stream.school_id == school_id,
                                Stream.grade_id == grade.id,
                            )
                        )
                    )
                    .scalars()
                    .all()
                )
                stream_map = {s.name: s for s in existing_streams}

                for str_data in g_data.streams:
                    stream = stream_map.get(str_data.name)
                    if not stream:
                        stream = Stream(school_id=school_id, grade_id=grade.id, name=str_data.name)
                        tenant_session.add(stream)
                        stream_map[str_data.name] = stream
                    grade_streams.append(stream)
                await tenant_session.flush()

                # Create Offerings for Streams
                for str_data in g_data.streams:
                    stream = stream_map[str_data.name]
                    for sub_data in str_data.subjects:
                        subject = subject_map[sub_data.code]
                        offering = SubjectOffering(
                            school_id=school_id,
                            year_id=year_id,
                            subject_id=subject.id,
                            grade_id=grade.id,
                            stream_id=stream.id,
                            assessment_scheme_id=scheme.id,
                        )
                        tenant_session.add(offering)

            else:
                # Offerings for Grade without Streams
                for sub_data in g_data.subjects:
                    subject = subject_map[sub_data.code]
                    offering = SubjectOffering(
                        school_id=school_id,
                        year_id=year_id,
                        subject_id=subject.id,
                        grade_id=grade.id,
                        stream_id=None,
                        assessment_scheme_id=scheme.id,
                    )
                    tenant_session.add(offering)

            # ClassSections
            if grade.has_stream and grade_streams:
                for i, section in enumerate(grade_sections):
                    stream = grade_streams[i % len(grade_streams)]
                    cs = ClassSection(
                        school_id=school_id,
                        academic_year_id=year_id,
                        section_id=section.id,
                        stream_id=stream.id,
                    )
                    tenant_session.add(cs)
            else:
                for section in grade_sections:
                    cs = ClassSection(
                        school_id=school_id,
                        academic_year_id=year_id,
                        section_id=section.id,
                        stream_id=None,
                    )
                    tenant_session.add(cs)

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
            maps.terms[term.id] = new_term.id
            tenant_session.add(new_term)
        await tenant_session.flush()

        # update the term ids to new uuids inside maps.terms for components lookup
        for idx, term in enumerate(previous_terms):
            maps.terms[term.id] = new_terms[idx].id

        # reusing existing Subjects, Grades, Sections, Streams as they are school scoped
        # need to map them to themselves so offerings can be copied
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

            for idx, scheme in enumerate(previous_schemes):
                maps.assessment_schemes[scheme.id] = new_schemes[idx].id

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

            for component in previous_components:
                # Need to map the old term to the new term
                # However, old component term might be from a different year.
                # Actually, the old term name (e.g. FIRST_TERM) maps to new term name.
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
                tenant_session.add(new_component)
                maps.assessment_scheme_components[component.id] = new_component.id
            await tenant_session.flush()

        # Copy SubjectOfferings
        for offering in previous_offerings:
            new_offering = SubjectOffering(
                school_id=school_id,
                year_id=year_id,
                subject_id=offering.subject_id,
                grade_id=offering.grade_id,
                stream_id=offering.stream_id,
                assessment_scheme_id=maps.assessment_schemes.get(
                    offering.assessment_scheme_id, offering.assessment_scheme_id
                ),
            )
            tenant_session.add(new_offering)
            maps.subject_offerings[offering.id] = new_offering.id
        await tenant_session.flush()

        # Copy ClassSections
        previous_class_sections = (
            (
                await tenant_session.execute(
                    select(ClassSection).where(ClassSection.academic_year_id == previous_year.id)
                )
            )
            .scalars()
            .all()
        )

        for cs in previous_class_sections:
            new_cs = ClassSection(
                school_id=school_id,
                section_id=cs.section_id,
                stream_id=cs.stream_id,
                academic_year_id=year_id,
                homeroom_teacher_id=None,
            )
            tenant_session.add(new_cs)
            maps.class_sections[cs.id] = new_cs.id
        await tenant_session.flush()

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

        subject_by_name: dict[str, Subject] = {}
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

        grade_by_value: dict[uuid.UUID, Grade] = {}
        stream_by_scope: dict[tuple[str, str], Stream] = {}
        sections: list[Section] = []
        streams: list[Stream] = []
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

            for section_name in DEFAULT_BLUEPRINT_SECTIONS:
                sections.append(
                    Section(
                        school_id=None,
                        grade_id=grade.id,
                        section=section_name,
                    )
                )

            if grade_data.streams:
                for stream_data in grade_data.streams:
                    stream = Stream(
                        school_id=None,
                        grade_id=grade.id,
                        name=stream_data.name,
                    )
                    system_session.add(stream)
                    await system_session.flush()
                    stream_by_scope[(grade.grade.value, stream.name)] = stream
                    streams.append(stream)

                    for subject_data in stream_data.subjects:
                        offerings.append(
                            SubjectOffering(
                                school_id=None,
                                year_id=blueprint_year.id,
                                subject_id=subject_by_name[subject_data.name].id,
                                grade_id=grade.id,
                                stream_id=stream.id,
                                assessment_scheme_id=scheme.id,
                            )
                        )
            else:
                for subject_data in grade_data.subjects:
                    offerings.append(
                        SubjectOffering(
                            school_id=None,
                            year_id=blueprint_year.id,
                            subject_id=subject_by_name[subject_data.name].id,
                            grade_id=grade.id,
                            stream_id=None,
                            assessment_scheme_id=scheme.id,
                        )
                    )

        system_session.add_all(sections)
        system_session.add_all(offerings)
        await system_session.flush()

        streams_by_grade: dict[uuid.UUID, list[Stream]] = {}
        for stream in streams:
            streams_by_grade.setdefault(stream.grade_id, []).append(stream)

        for section in sections:
            grade = grade_by_value.get(section.grade_id)

            if grade and grade.has_stream:
                available_streams = streams_by_grade.get(section.grade_id, [])

                if available_streams:
                    # Use modulo to cycle through streams repeatedly
                    stream_index = sections.index(section) % len(available_streams)
                    assigned_stream = available_streams[stream_index]

                    class_sections.append(
                        ClassSection(
                            school_id=None,
                            section_id=section.id,
                            stream_id=assigned_stream.id,
                            academic_year_id=blueprint_year.id,
                        )
                    )
            else:
                class_sections.append(
                    ClassSection(
                        school_id=None,
                        section_id=section.id,
                        stream_id=None,
                        academic_year_id=blueprint_year.id,
                    )
                )

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
        rows: Iterable,
        key_fields: tuple[str, ...],
    ) -> dict[tuple, T]:
        tenant_rows = (await tenant_session.execute(select(model).where(model.school_id == school_id))).scalars().all()
        return {
            tuple(getattr(row, field) for field in key_fields): row
            for row in tenant_rows
            if tuple(getattr(row, field) for field in key_fields)
            in {tuple(getattr(source, field) for field in key_fields) for source in rows}
        }

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
        new_rows: list[Year] = []
        for year in years:
            new_year = Year(
                school_id=None,
                calendar_type=year.calendar_type,
                name=year.name.replace(" Blueprint", ""),
                start_date=year.start_date,
                end_date=year.end_date,
                status=year.status,
            )
            new_year.school_id = school_id
            maps.years[year.id] = new_year.id
            new_rows.append(new_year)
        tenant_session.add_all(new_rows)
        await tenant_session.flush()

    @classmethod
    async def _copy_terms(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        terms = await cls._blueprint_rows(system_session=system_session, model=AcademicTerm)
        new_rows: list[AcademicTerm] = []
        for term in terms:
            if term.year_id not in maps.years:
                continue
            new_term = AcademicTerm(
                school_id=None,
                year_id=maps.years[term.year_id],
                name=term.name,
                start_date=term.start_date,
                end_date=term.end_date,
                registration_start=term.registration_start,
                registration_end=term.registration_end,
            )
            new_term.school_id = school_id
            maps.terms[term.id] = new_term.id
            new_rows.append(new_term)
        tenant_session.add_all(new_rows)
        await tenant_session.flush()

    @classmethod
    async def _ensure_terms(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        terms = await cls._blueprint_rows(system_session=system_session, model=AcademicTerm)
        tenant_year_ids = set(maps.years.values())
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
        for term in terms:
            tenant_year_id = maps.years.get(term.year_id)
            if tenant_year_id is None:
                continue
            tenant_term = existing.get((tenant_year_id, term.name))
            if tenant_term is None:
                tenant_term = AcademicTerm(
                    school_id=None,
                    year_id=tenant_year_id,
                    name=term.name,
                    start_date=term.start_date,
                    end_date=term.end_date,
                    registration_start=term.registration_start,
                    registration_end=term.registration_end,
                )
                tenant_term.school_id = school_id
                new_rows.append(tenant_term)
            maps.terms[term.id] = tenant_term.id
        tenant_session.add_all(new_rows)
        await tenant_session.flush()

    @classmethod
    async def _copy_subjects(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        subjects = await cls._blueprint_rows(system_session=system_session, model=Subject)
        new_rows: list[Subject] = []
        for subject in subjects:
            new_subject = Subject(
                school_id=None,
                name=subject.name,
                code=subject.code,
            )
            new_subject.school_id = school_id
            maps.subjects[subject.id] = new_subject.id
            new_rows.append(new_subject)
        tenant_session.add_all(new_rows)
        await tenant_session.flush()

    @classmethod
    async def _ensure_subjects(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        subjects = await cls._blueprint_rows(system_session=system_session, model=Subject)
        existing = await cls._tenant_rows_by_key(tenant_session, Subject, school_id, subjects, ("code",))
        new_rows: list[Subject] = []
        for subject in subjects:
            tenant_subject = existing.get((subject.code,))
            if tenant_subject is None:
                tenant_subject = Subject(
                    school_id=None,
                    name=subject.name,
                    code=subject.code,
                )
                tenant_subject.school_id = school_id
                new_rows.append(tenant_subject)
            maps.subjects[subject.id] = tenant_subject.id
        tenant_session.add_all(new_rows)
        await tenant_session.flush()

    @classmethod
    async def _copy_grades(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        grades = await cls._blueprint_rows(system_session=system_session, model=Grade)
        new_rows: list[Grade] = []
        for grade in grades:
            new_grade = Grade(
                school_id=None,
                grade=grade.grade,
                level=grade.level,
                has_stream=grade.has_stream,
            )
            new_grade.school_id = school_id
            maps.grades[grade.id] = new_grade.id
            new_rows.append(new_grade)
        tenant_session.add_all(new_rows)
        await tenant_session.flush()

    @classmethod
    async def _ensure_grades(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        grades = await cls._blueprint_rows(system_session=system_session, model=Grade)
        tenant_grades = (
            (await tenant_session.execute(select(Grade).where(Grade.school_id == school_id))).scalars().all()
        )
        existing = {grade.grade: grade for grade in tenant_grades}
        new_rows: list[Grade] = []
        for grade in grades:
            tenant_grade = existing.get(grade.grade)
            if tenant_grade is None:
                tenant_grade = Grade(
                    school_id=None,
                    grade=grade.grade,
                    level=grade.level,
                    has_stream=grade.has_stream,
                )
                tenant_grade.school_id = school_id
                new_rows.append(tenant_grade)
            maps.grades[grade.id] = tenant_grade.id
        tenant_session.add_all(new_rows)
        await tenant_session.flush()

    @classmethod
    async def _copy_sections(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        sections = await cls._blueprint_rows(system_session=system_session, model=Section)
        new_rows: list[Section] = []
        for section in sections:
            if section.grade_id not in maps.grades:
                continue
            new_section = Section(
                school_id=None,
                grade_id=maps.grades[section.grade_id],
                section=section.section,
            )
            new_section.school_id = school_id
            maps.sections[section.id] = new_section.id
            new_rows.append(new_section)
        tenant_session.add_all(new_rows)
        await tenant_session.flush()

    @classmethod
    async def _ensure_sections(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        sections = await cls._blueprint_rows(system_session=system_session, model=Section)
        tenant_sections = (
            (await tenant_session.execute(select(Section).where(Section.school_id == school_id))).scalars().all()
        )
        existing = {(section.grade_id, section.section): section for section in tenant_sections}
        new_rows: list[Section] = []
        for section in sections:
            tenant_grade_id = maps.grades.get(section.grade_id)
            if tenant_grade_id is None:
                continue
            tenant_section = existing.get((tenant_grade_id, section.section))
            if tenant_section is None:
                tenant_section = Section(
                    school_id=None,
                    grade_id=tenant_grade_id,
                    section=section.section,
                )
                tenant_section.school_id = school_id
                new_rows.append(tenant_section)
            maps.sections[section.id] = tenant_section.id
        tenant_session.add_all(new_rows)
        await tenant_session.flush()

    @classmethod
    async def _copy_streams(
        cls,
        *,
        tenant_session: AsyncSession,
        system_session: AsyncSession,
        school_id: uuid.UUID,
        maps: ProvisioningMaps,
    ) -> None:
        streams = await cls._blueprint_rows(system_session=system_session, model=Stream)
        new_rows: list[Stream] = []
        for stream in streams:
            if stream.grade_id not in maps.grades:
                continue
            new_stream = Stream(
                school_id=None,
                grade_id=maps.grades[stream.grade_id],
                name=stream.name,
            )
            new_stream.school_id = school_id
            maps.streams[stream.id] = new_stream.id
            new_rows.append(new_stream)
        tenant_session.add_all(new_rows)
        await tenant_session.flush()

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
        existing = {(stream.grade_id, stream.name): stream for stream in tenant_streams}
        new_rows: list[Stream] = []
        for stream in streams:
            tenant_grade_id = maps.grades.get(stream.grade_id)
            if tenant_grade_id is None:
                continue
            tenant_stream = existing.get((tenant_grade_id, stream.name))
            if tenant_stream is None:
                tenant_stream = Stream(
                    school_id=None,
                    grade_id=tenant_grade_id,
                    name=stream.name,
                )
                tenant_stream.school_id = school_id
                new_rows.append(tenant_stream)
            maps.streams[stream.id] = tenant_stream.id
        tenant_session.add_all(new_rows)
        await tenant_session.flush()

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
        new_rows: list[AssessmentScheme] = []
        for scheme in schemes:
            name = scheme.name if name_suffix is None else f"{scheme.name} - {name_suffix}"
            new_scheme = AssessmentScheme(
                school_id=None,
                name=name,
                description=scheme.description,
            )
            new_scheme.school_id = school_id
            maps.assessment_schemes[scheme.id] = new_scheme.id
            new_rows.append(new_scheme)
        tenant_session.add_all(new_rows)
        await tenant_session.flush()

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
        new_rows: list[AssessmentSchemeComponent] = []
        for component in components:
            if component.term_id not in maps.terms or component.assessment_scheme_id not in maps.assessment_schemes:
                continue
            new_component = AssessmentSchemeComponent(
                school_id=None,
                term_id=maps.terms[component.term_id],
                assessment_scheme_id=maps.assessment_schemes[component.assessment_scheme_id],
                name=component.name,
                description=component.description,
                weight=component.weight,
                max_score=component.max_score,
                display_order=component.display_order,
            )
            new_component.school_id = school_id
            maps.assessment_scheme_components[component.id] = new_component.id
            new_rows.append(new_component)
        tenant_session.add_all(new_rows)
        await tenant_session.flush()

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
        new_rows: list[SubjectOffering] = []
        school = (await tenant_session.execute(select(School).where(School.id == school_id))).scalar_one_or_none()
        if school is None:
            raise ValueError(f"School with id {school_id} not found.")

        for offering in offerings:
            if (
                offering.year_id not in maps.years
                or offering.subject_id not in maps.subjects
                or offering.grade_id not in maps.grades
                or offering.assessment_scheme_id not in maps.assessment_schemes
            ):
                continue
            if offering.stream_id is not None and offering.stream_id not in maps.streams:
                continue

            stream_id = None
            stream = None
            if offering.stream_id is not None:
                stream = (
                    await tenant_session.execute(select(Stream).where(Stream.id == maps.streams[offering.stream_id]))
                ).scalar_one_or_none()
                if stream is None:
                    raise ValueError(
                        "Can not find Stream with id, ",
                        maps.streams[offering.stream_id],
                    )

                stream_id = stream.id

            new_offering = SubjectOffering(
                school_id=None,
                year_id=maps.years[offering.year_id],
                subject_id=maps.subjects[offering.subject_id],
                grade_id=maps.grades[offering.grade_id],
                stream_id=stream_id,
                assessment_scheme_id=maps.assessment_schemes[offering.assessment_scheme_id],
            )
            new_offering.stream_id = stream_id
            new_offering.school_id = school_id

            maps.subject_offerings[offering.id] = new_offering.id
            new_rows.append(new_offering)
        tenant_session.add_all(new_rows)
        await tenant_session.flush()
        pass

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
        new_rows: list[ClassSection] = []
        for class_section in class_sections:
            if class_section.section_id not in maps.sections or class_section.academic_year_id not in maps.years:
                continue
            if class_section.stream_id is not None and class_section.stream_id not in maps.streams:
                continue

            stream_id = None
            if class_section.stream_id is not None:
                stream_id = maps.streams[class_section.stream_id]

            new_class_section = ClassSection(
                school_id=None,
                section_id=maps.sections[class_section.section_id],
                stream_id=stream_id,
                academic_year_id=maps.years[class_section.academic_year_id],
                homeroom_teacher_id=None,
            )
            new_class_section.school_id = school_id
            maps.class_sections[class_section.id] = new_class_section.id
            new_rows.append(new_class_section)
        tenant_session.add_all(new_rows)
        await tenant_session.flush()
