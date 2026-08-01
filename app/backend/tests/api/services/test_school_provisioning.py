import uuid
from collections.abc import Iterable
from typing import TypeVar

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import _count_rows

from project.models import (
    AcademicTerm,
    AssessmentScheme,
    AssessmentSchemeComponent,
    ClassSection,
    Grade,
    School,
    Section,
    Stream,
    Subject,
    SubjectOffering,
    Year,
)
from project.models.base.school_mixin import SchoolScopedMixin
from project.services.school_provisioning import (
    DEFAULT_BLUEPRINT_SCHEME_NAME,
    DEFAULT_BLUEPRINT_YEAR_NAME,
    ProvisioningMaps,
    SchoolAlreadyProvisionedError,
    SchoolProvisioningError,
    SchoolProvisioningService,
)
from project.utils.enum import (
    AcademicTermEnum,
    AcademicTermTypeEnum,
    AcademicYearStatusEnum,
    SchoolStatusEnum,
)

pytestmark = pytest.mark.asyncio


PROVISIONED_MODELS = (
    Year,
    AcademicTerm,
    Subject,
    Grade,
    Section,
    Stream,
    AssessmentScheme,
    AssessmentSchemeComponent,
    SubjectOffering,
    ClassSection,
)

T = TypeVar("T", bound=SchoolScopedMixin)


async def _create_school(session: AsyncSession, name_prefix: str) -> School:
    suffix = uuid.uuid4().hex[:12]
    school = School(
        name=f"{name_prefix} {suffix}",
        slug=f"{name_prefix.lower().replace(' ', '-')}-{suffix}",
        status=SchoolStatusEnum.ACTIVE,
        settings={"test": "school-provisioning"},
    )
    session.add(school)
    await session.flush()
    return school


async def _rows(
    *,
    system_session: AsyncSession,
    model: type[T],
    school_id: uuid.UUID | None = None,
) -> list:
    """
    Fetches all rows of a given model, optionally filtered by school_id.
    """
    if school_id is None:
        return (await system_session.execute(select(model).where(model.school_id.is_(None)))).scalars().all()

    return (await system_session.execute(select(model).where(model.school_id == school_id))).scalars().all()


def _assert_map_is_complete(
    source_rows: Iterable,
    mapping: dict[uuid.UUID, uuid.UUID],
) -> None:
    source_ids = {row.id for row in source_rows}
    assert set(mapping) == source_ids
    assert not source_ids.intersection(mapping.values())


async def test_ensure_default_blueprint_creates_complete_global_blueprint(
    db_session: AsyncSession,
    system_db_session: AsyncSession,
) -> None:
    await SchoolProvisioningService.ensure_default_blueprint(system_session=system_db_session)

    blueprint_year = (
        await db_session.execute(
            select(Year).where(
                Year.school_id.is_(None),
                Year.name == DEFAULT_BLUEPRINT_YEAR_NAME,
            )
        )
    ).scalar_one()

    assert blueprint_year.calendar_type == AcademicTermTypeEnum.SEMESTER
    assert blueprint_year.status == AcademicYearStatusEnum.UPCOMING

    counts = {
        model.__tablename__: await _count_rows(
            tenant_session=db_session,
            model=model,
            school_id=None,
        )
        for model in PROVISIONED_MODELS
    }

    assert counts["years"] == 1
    assert counts["academic_terms"] == 2
    assert counts["subjects"] >= 20
    assert counts["grades"] == 12
    assert counts["sections"] >= 36
    assert counts["streams"] >= 2
    assert counts["assessment_schemes"] == 1
    assert counts["assessment_scheme_components"] == 4
    assert counts["subject_offerings"] == 130
    assert counts["class_sections"] > 0

    # The seed operation is idempotent and does not add duplicate blueprint rows.
    await SchoolProvisioningService.ensure_default_blueprint(system_session=system_db_session)
    assert counts == {
        model.__tablename__: await _count_rows(
            tenant_session=db_session,
            model=model,
            school_id=None,
        )
        for model in PROVISIONED_MODELS
    }


async def test_setup_school_copies_blueprint_rows_and_returns_complete_id_maps(
    db_session: AsyncSession,
    system_db_session: AsyncSession,
) -> None:
    school = await _create_school(db_session, "Provisioning Full Copy")

    maps = await SchoolProvisioningService.setup_school(
        tenant_session=db_session,
        system_session=system_db_session,
        school_id=school.id,
    )

    assert isinstance(maps, ProvisioningMaps)
    for model, mapping in (
        (Year, maps.years),
        (AcademicTerm, maps.terms),
        (Subject, maps.subjects),
        (Grade, maps.grades),
        (Section, maps.sections),
        (Stream, maps.streams),
        (AssessmentScheme, maps.assessment_schemes),
        (AssessmentSchemeComponent, maps.assessment_scheme_components),
        (SubjectOffering, maps.subject_offerings),
        (ClassSection, maps.class_sections),
    ):
        blueprint_rows = await _rows(system_session=system_db_session, model=model)
        tenant_rows = await _rows(
            system_session=db_session,
            model=model,
            school_id=school.id,
        )
        assert len(tenant_rows) == len(blueprint_rows)
        _assert_map_is_complete(blueprint_rows, mapping)


async def test_setup_school_remaps_all_copied_foreign_keys_to_tenant_rows(
    db_session: AsyncSession,
    system_db_session: AsyncSession,
) -> None:
    school = await _create_school(db_session, "Provisioning FK Remap")

    maps = await SchoolProvisioningService.setup_school(
        tenant_session=db_session,
        system_session=system_db_session,
        school_id=school.id,
    )

    tenant_terms = await _rows(
        system_session=db_session,
        model=AcademicTerm,
        school_id=school.id,
    )
    assert {term.year_id for term in tenant_terms} == set(maps.years.values())

    tenant_sections = await _rows(
        system_session=db_session,
        model=Section,
        school_id=school.id,
    )
    assert {section.grade_id for section in tenant_sections}.issubset(set(maps.grades.values()))

    tenant_streams = await _rows(
        system_session=db_session,
        model=Stream,
        school_id=school.id,
    )
    assert {stream.grade_id for stream in tenant_streams}.issubset(set(maps.grades.values()))

    tenant_components = await _rows(
        system_session=db_session,
        model=AssessmentSchemeComponent,
        school_id=school.id,
    )
    assert {component.term_id for component in tenant_components}.issubset(set(maps.terms.values()))
    assert {component.assessment_scheme_id for component in tenant_components}.issubset(
        set(maps.assessment_schemes.values())
    )

    tenant_offerings = await _rows(
        system_session=db_session,
        model=SubjectOffering,
        school_id=school.id,
    )
    assert {offering.year_id for offering in tenant_offerings}.issubset(set(maps.years.values()))
    assert {offering.subject_id for offering in tenant_offerings}.issubset(set(maps.subjects.values()))
    assert {offering.grade_id for offering in tenant_offerings}.issubset(set(maps.grades.values()))
    assert {offering.assessment_scheme_id for offering in tenant_offerings}.issubset(
        set(maps.assessment_schemes.values())
    )
    assert {offering.stream_id for offering in tenant_offerings if offering.stream_id}.issubset(
        set(maps.streams.values())
    )

    tenant_class_sections = await _rows(
        system_session=db_session,
        model=ClassSection,
        school_id=school.id,
    )
    assert {class_section.section_id for class_section in tenant_class_sections}.issubset(set(maps.sections.values()))
    assert {class_section.academic_year_id for class_section in tenant_class_sections}.issubset(
        set(maps.years.values())
    )
    assert {class_section.stream_id for class_section in tenant_class_sections if class_section.stream_id}.issubset(
        set(maps.streams.values())
    )


async def test_setup_school_creates_independent_tenant_copies(
    db_session: AsyncSession,
    system_db_session: AsyncSession,
) -> None:
    school = await _create_school(db_session, "Provisioning Independence")

    maps = await SchoolProvisioningService.setup_school(
        tenant_session=db_session, system_session=system_db_session, school_id=school.id
    )
    blueprint_subject_id, tenant_subject_id = next(iter(maps.subjects.items()))

    blueprint_subject = await db_session.get(Subject, blueprint_subject_id)
    tenant_subject = await db_session.get(Subject, tenant_subject_id)
    assert blueprint_subject is not None
    assert tenant_subject is not None

    tenant_subject.name = "Tenant Edited Subject"
    await db_session.flush()
    await db_session.refresh(blueprint_subject)

    assert blueprint_subject.name != tenant_subject.name
    assert blueprint_subject.school_id is None
    assert tenant_subject.school_id == school.id


async def test_setup_school_fails_safely_when_school_already_has_provisioned_data(
    db_session: AsyncSession,
    system_db_session: AsyncSession,
) -> None:
    school = await _create_school(db_session, "Provisioning Duplicate")

    await SchoolProvisioningService.setup_school(
        tenant_session=db_session, system_session=system_db_session, school_id=school.id
    )

    with pytest.raises(SchoolAlreadyProvisionedError):
        await SchoolProvisioningService.setup_school(
            tenant_session=db_session,
            system_session=system_db_session,
            school_id=school.id,
        )


async def test_setup_academic_year_from_blueprint_reuses_existing_configuration(
    db_session: AsyncSession,
    system_db_session: AsyncSession,
) -> None:
    school = await _create_school(db_session, "Provisioning Existing Config")
    initial_maps = await SchoolProvisioningService.setup_school(
        tenant_session=db_session,
        system_session=system_db_session,
        school_id=school.id,
    )

    subject_count = await _count_rows(tenant_session=db_session, model=Subject, school_id=school.id)
    grade_count = await _count_rows(tenant_session=db_session, model=Grade, school_id=school.id)
    section_count = await _count_rows(tenant_session=db_session, model=Section, school_id=school.id)
    stream_count = await _count_rows(tenant_session=db_session, model=Stream, school_id=school.id)

    initial_year = await db_session.get(Year, next(iter(initial_maps.years.values())))
    assert initial_year is not None

    year = Year(
        school_id=school.id,
        calendar_type=AcademicTermTypeEnum.SEMESTER,
        name=f"Follow Up Year {uuid.uuid4().hex[:8]}",
        start_date=initial_year.start_date,
        end_date=initial_year.end_date,
        status=AcademicYearStatusEnum.UPCOMING,
    )
    db_session.add(year)
    await db_session.flush()

    for term_name in (AcademicTermEnum.FIRST_TERM, AcademicTermEnum.SECOND_TERM):
        term = AcademicTerm(
            school_id=school.id,
            year_id=year.id,
            name=term_name,
            start_date=None,
            end_date=None,
            registration_start=None,
            registration_end=None,
        )
        db_session.add(term)
    await db_session.flush()

    maps = await SchoolProvisioningService.setup_academic_year_from_blueprint(
        tenant_session=db_session,
        system_session=system_db_session,
        school_id=school.id,
        year_id=year.id,
    )

    assert set(maps.subjects.values()).issubset(set(initial_maps.subjects.values()))
    assert set(maps.grades.values()).issubset(set(initial_maps.grades.values()))
    assert set(maps.sections.values()).issubset(set(initial_maps.sections.values()))
    assert set(maps.streams.values()).issubset(set(initial_maps.streams.values()))
    assert await _count_rows(tenant_session=db_session, model=Subject, school_id=school.id) == subject_count
    assert await _count_rows(tenant_session=db_session, model=Grade, school_id=school.id) == grade_count
    assert await _count_rows(tenant_session=db_session, model=Section, school_id=school.id) == section_count
    assert await _count_rows(tenant_session=db_session, model=Stream, school_id=school.id) == stream_count

    tenant_offerings = (
        (
            await db_session.execute(
                select(SubjectOffering).where(
                    SubjectOffering.school_id == school.id,
                    SubjectOffering.year_id == year.id,
                )
            )
        )
        .scalars()
        .all()
    )
    assert len(tenant_offerings) == len(maps.subject_offerings)
    assert tenant_offerings

    schemes = (
        (
            await db_session.execute(
                select(AssessmentScheme).where(
                    AssessmentScheme.school_id == school.id,
                    AssessmentScheme.name == f"{DEFAULT_BLUEPRINT_SCHEME_NAME} - {year.name}",
                )
            )
        )
        .scalars()
        .all()
    )
    assert len(schemes) == 1


async def test_private_helpers_raise_for_missing_required_blueprint_or_year(
    db_session: AsyncSession,
    system_db_session: AsyncSession,
) -> None:
    missing_year_id = uuid.uuid4()

    with pytest.raises(SchoolProvisioningError):
        await SchoolProvisioningService._year_name(
            tenant_session=db_session,
            year_id=missing_year_id,
        )

    # required=False is the non-raising branch used by ensure_default_blueprint.
    assert (
        await SchoolProvisioningService._get_blueprint_year_id(
            system_session=system_db_session,
            required=False,
        )
        is not None
    )
