import uuid
from typing import List

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from project.api.v1.routers.dependencies import AuthenticatedRoute, SessionDep
from project.models import (
    AcademicTerm,
    AssessmentScheme,
    AssessmentSchemeComponent,
    ClassSection,
    Grade,
    GradeStream,
    Section,
    Stream,
    Subject,
    SubjectOffering,
)
from project.schema.schema import SuccessMessage
from project.services.school_provisioning import SchoolProvisioningService
from project.utils.enum import PermissionEnum, RoleEnum

from .schema import (
    AssessmentComponentCreateSchema,
    AssessmentSchemeCreateSchema,
    ClassSectionCreateSchema,
    GradeCreateSchema,
    ManualSetupBulkSchema,
    SectionCreateSchema,
    StreamCreateSchema,
    SubjectCreateSchema,
    SubjectOfferingCreateSchema,
    TermCreateSchema,
)

router = APIRouter(prefix="/academic-setup", tags=["Academic Setup"])


def check_permission(user_in: AuthenticatedRoute):
    if not user_in.has_role(RoleEnum.ADMIN) and not user_in.has_permission(PermissionEnum.YEARS_WRITE):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@router.post("/terms", response_model=SuccessMessage, status_code=status.HTTP_201_CREATED)
async def create_terms(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    year_id: uuid.UUID,
    terms: List[TermCreateSchema],
):
    check_permission(user_in)
    try:
        for t in terms:
            term = AcademicTerm(
                school_id=user_in.membership.school_id,
                year_id=year_id,
                name=t.name,
                start_date=t.start_date,
                end_date=t.end_date,
                registration_start=t.registration_start,
                registration_end=t.registration_end,
            )
            session.add(term)
        await session.commit()
        return SuccessMessage(message="Terms created successfully")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/subjects", response_model=SuccessMessage, status_code=status.HTTP_201_CREATED)
async def create_subjects(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    subjects: List[SubjectCreateSchema],
):
    check_permission(user_in)
    try:
        for s in subjects:
            subject = Subject(
                school_id=user_in.membership.school_id,
                name=s.name,
                code=s.code,
            )
            session.add(subject)
        await session.commit()
        return SuccessMessage(message="Subjects created successfully")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/grades", response_model=SuccessMessage, status_code=status.HTTP_201_CREATED)
async def create_grades(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    grades: List[GradeCreateSchema],
):
    check_permission(user_in)
    try:
        for g in grades:
            grade = Grade(
                school_id=user_in.membership.school_id,
                grade=g.grade,
                level=g.level,
                has_stream=g.has_stream,
            )
            session.add(grade)
        await session.commit()
        return SuccessMessage(message="Grades created successfully")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sections", response_model=SuccessMessage, status_code=status.HTTP_201_CREATED)
async def create_sections(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    sections: List[SectionCreateSchema],
):
    check_permission(user_in)
    try:
        for s in sections:
            section = Section(
                school_id=user_in.membership.school_id,
                grade_id=s.grade_id,
                section=s.section,
            )
            session.add(section)
        await session.commit()
        return SuccessMessage(message="Sections created successfully")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/streams", response_model=SuccessMessage, status_code=status.HTTP_201_CREATED)
async def create_streams(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    streams: List[StreamCreateSchema],
):
    check_permission(user_in)
    try:
        for s in streams:
            stream = Stream(
                school_id=user_in.membership.school_id,
                name=s.name,
            )
            session.add(stream)
        await session.commit()
        return SuccessMessage(message="Streams created successfully")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/assessment-schemes",
    response_model=SuccessMessage,
    status_code=status.HTTP_201_CREATED,
)
async def create_assessment_schemes(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    schemes: List[AssessmentSchemeCreateSchema],
):
    check_permission(user_in)
    try:
        for s in schemes:
            scheme = AssessmentScheme(
                school_id=user_in.membership.school_id,
                name=s.name,
                description=s.description,
            )
            session.add(scheme)
        await session.commit()
        return SuccessMessage(message="Assessment schemes created successfully")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/assessment-components",
    response_model=SuccessMessage,
    status_code=status.HTTP_201_CREATED,
)
async def create_assessment_components(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    components: List[AssessmentComponentCreateSchema],
):
    check_permission(user_in)
    try:
        for c in components:
            comp = AssessmentSchemeComponent(
                school_id=user_in.membership.school_id,
                term_id=c.term_id,
                assessment_scheme_id=c.assessment_scheme_id,
                name=c.name,
                description=c.description,
                weight=c.weight,
                max_score=c.max_score,
                display_order=c.display_order,
            )
            session.add(comp)
        await session.commit()
        return SuccessMessage(message="Assessment components created successfully")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/subject-offerings",
    response_model=SuccessMessage,
    status_code=status.HTTP_201_CREATED,
)
async def create_subject_offerings(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    offerings: List[SubjectOfferingCreateSchema],
):
    check_permission(user_in)
    try:
        for o in offerings:
            grade_stream = (
                await session.execute(
                    select(GradeStream).where(GradeStream.grade_id == o.grade_id, GradeStream.stream_id == o.stream_id)
                )
            ).scalar_one_or_none()

            if not grade_stream:
                raise HTTPException(
                    status_code=400,
                    detail=f"Grade or Stream not found for grade_id {o.grade_id} and stream_id {o.stream_id}",
                )

            offering = SubjectOffering(
                school_id=user_in.membership.school_id,
                year_id=o.year_id,
                subject_id=o.subject_id,
                grade_stream_id=grade_stream.id,
                assessment_scheme_id=o.assessment_scheme_id,
            )
            session.add(offering)
        await session.commit()
        return SuccessMessage(message="Subject offerings created successfully")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/class-sections",
    response_model=SuccessMessage,
    status_code=status.HTTP_201_CREATED,
)
async def create_class_sections(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    class_sections: List[ClassSectionCreateSchema],
):
    check_permission(user_in)
    try:
        for cs in class_sections:
            grade_stream = (
                await session.execute(
                    select(GradeStream).where(
                        GradeStream.grade_id == cs.grade_id, GradeStream.stream_id == cs.stream_id
                    )
                )
            ).scalar_one_or_none()

            if not grade_stream:
                raise HTTPException(
                    status_code=400,
                    detail=f"Grade or Stream not found for grade_id {cs.grade_id} and stream_id {cs.stream_id}",
                )

            class_section = ClassSection(
                school_id=user_in.membership.school_id,
                academic_year_id=cs.academic_year_id,
                section_id=cs.section_id,
                grade_stream_id=grade_stream.id,
            )
            session.add(class_section)
        await session.commit()
        return SuccessMessage(message="Class sections created successfully")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bulk", response_model=SuccessMessage, status_code=status.HTTP_201_CREATED)
async def setup_manual_bulk(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    payload: ManualSetupBulkSchema,
):
    check_permission(user_in)
    try:
        await SchoolProvisioningService.setup_academic_year_from_payload(
            tenant_session=session,
            school_id=user_in.membership.school_id,
            year_id=payload.year_id,
            blueprint=payload.blueprint,
        )
        await session.commit()
        return SuccessMessage(message="Bulk setup completed successfully")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
