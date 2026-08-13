import uuid
from typing import Annotated, Any, Dict, List, Sequence

from fastapi import APIRouter, HTTPException, Query
from fastapi.logger import logger
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from project.api.v1.routers.dependencies import (
    AuthenticatedRoute,
    SessionDep,
)
from project.api.v1.routers.schema import FilterParams
from project.api.v1.routers.subjects.schema import (
    NewSubject,
    NewSubjectSuccess,
    SubjectSetupSchema,
    UpdateSubjectSetup,
    UpdateSubjectSetupSuccess,
)
from project.api.v1.routers.subjects.service import update_subject_relationships
from project.models import GradeStream, SubjectOffering
from project.models.subject import Subject
from project.models.year import Year
from project.schema.models.subject_schema import (
    SubjectSchema,
)
from project.utils.enum import PermissionEnum

router = APIRouter(tags=["Subjects"])


@router.get(
    "/subjects",
    response_model=List[SubjectSchema],
)
async def get_subjects(
    session: SessionDep,
    user_in: AuthenticatedRoute,
) -> Sequence[Subject]:
    """
    Returns All Subjects with in academic year
    """
    if not user_in.has_permission(PermissionEnum.SUBJECTS_READ):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to read subjects.",
        )

    subjects = (await session.execute(select(Subject).order_by(Subject.name))).scalars().all()

    return subjects


@router.post(
    "/subjects",
    response_model=NewSubjectSuccess,
)
async def post_subject(
    session: SessionDep,
    new_subject: NewSubject,
    user_in: AuthenticatedRoute,
) -> Dict[str, Any]:
    """
    Creates a new Subject
    """
    if not user_in.has_permission(PermissionEnum.SUBJECTS_WRITE):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to write subjects.",
        )

    existing_subject_name = (
        (
            await session.execute(
                select(Subject).where(
                    Subject.name == new_subject.name,
                )
            )
        )
        .scalars()
        .first()
    )

    if existing_subject_name:
        raise HTTPException(status_code=400, detail="Subject name for the school already exists.")

    existing_subject_code = (
        (
            await session.execute(
                select(Subject).where(
                    Subject.code == new_subject.code,
                )
            )
        )
        .scalars()
        .first()
    )

    if existing_subject_code:
        raise HTTPException(status_code=400, detail="Subject code for the school already exists.")

    try:
        subject = Subject(
            school_id=user_in.membership.school_id,
            name=new_subject.name,
            code=new_subject.code,
        )
        session.add(subject)
        await session.commit()
        await session.refresh(subject)

        return {"message": "Subject created Successfully", "id": subject.id}
    except Exception as e:
        logger.error(f"Error creating subject: {e}")
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Creation failed: {str(e)}")


@router.get(
    "/subject-offerings",
    response_model=List[SubjectSetupSchema],
)
async def get_subject_offerings(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    query: Annotated[FilterParams, Query()],
) -> Sequence[Subject]:
    """
    Returns All Subjects with in academic year
    """
    if not user_in.has_permission(PermissionEnum.SUBJECTS_READ):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to read subjects.",
        )

    year = await session.get(Year, query.year_id)
    if not year:
        raise HTTPException(status_code=404, detail="Academic year not found.")

    subject = select(Subject).join(Subject.subject_offerings).where(SubjectOffering.year_id == year.id)

    if query.q:
        subject = subject.where(Subject.name.ilike(f"%{query.q}%"))

    subject_offering = (
        (
            await session.execute(
                subject.options(
                    selectinload(Subject.subject_offerings)
                    .selectinload(SubjectOffering.grade_stream)
                    .selectinload(GradeStream.grade),
                    selectinload(Subject.subject_offerings)
                    .selectinload(SubjectOffering.grade_stream)
                    .selectinload(GradeStream.stream),
                )
                .group_by(Subject.id)
                .order_by(Subject.name)
            )
        )
        .scalars()
        .all()
    )

    return subject_offering


@router.get(
    "/subject-offerings/{subject_id}",
    response_model=SubjectSetupSchema,
)
async def get_subject_offerings_by_id(
    session: SessionDep,
    subject_id: uuid.UUID,
    user_in: AuthenticatedRoute,
) -> Subject:
    """
    Returns specific academic subject
    """
    if not user_in.has_permission(PermissionEnum.SUBJECTS_READ):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to read subjects.",
        )

    subject_offering = (
        await session.execute(
            select(Subject)
            .where(Subject.id == subject_id)
            .options(
                selectinload(Subject.subject_offerings)
                .selectinload(SubjectOffering.grade_stream)
                .selectinload(GradeStream.grade),
                selectinload(Subject.subject_offerings)
                .selectinload(SubjectOffering.grade_stream)
                .selectinload(GradeStream.stream),
            )
            .group_by(Subject.id)
            .order_by(Subject.name)
        )
    ).scalar_one_or_none()

    if not subject_offering:
        raise HTTPException(
            status_code=404,
            detail=f"Subject with ID {subject_id} not found.",
        )

    return subject_offering


@router.patch(
    "/subjects/setup/{subject_id}",
    response_model=UpdateSubjectSetupSuccess,
)
async def patch_subject_setup(
    session: SessionDep,
    subject_id: uuid.UUID,
    update_data: UpdateSubjectSetup,
    user_in: AuthenticatedRoute,
) -> Dict[str, str]:
    """
    Updates Subject SetUp
    """
    subject = await session.get(Subject, subject_id)
    if not subject:
        raise HTTPException(
            status_code=404,
            detail=f"Subject with ID {subject_id} not found.",
        )

    try:
        # Update simple fields
        for key in update_data.model_fields_set - {
            "grades",
            "streams",
        }:
            if hasattr(subject, key):
                setattr(subject, key, getattr(update_data, key))

        # Update relationships
        update_subject_relationships(
            year_id=uuid.UUID(),  # TODO: Pass actual year_id from request context
            subject=subject,
            update_data=update_data,
            session=session,
        )

        await session.commit()

        return {"message": "Subject Setup Updated Successfully"}
    except Exception as e:
        logger.error(f"Error updating subject setup: {e}")
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")


@router.get(
    "/subjects/{subject_id}",
    response_model=SubjectSchema,
)
async def get_subject_by_id(
    session: SessionDep,
    subject_id: uuid.UUID,
    user_in: AuthenticatedRoute,
) -> Subject:
    """
    Returns specific academic subject
    """
    subject = await session.get(Subject, subject_id)
    if not subject:
        raise HTTPException(
            status_code=404,
            detail=f"Subject with ID {subject_id} not found.",
        )

    return subject
