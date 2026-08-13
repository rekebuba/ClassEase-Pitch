import re
import uuid
from typing import Annotated, Any, Dict, List, Sequence

from fastapi import APIRouter, HTTPException, Query
from fastapi.logger import logger
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from project.api.v1.routers.dependencies import (
    AuthenticatedRoute,
    SessionDep,
)
from project.api.v1.routers.grades.schema import (
    GradeSetupSchema,
    NewGrade,
    NewGradeSuccess,
    UpdateGradeSetup,
    UpdateGradeSetupSuccess,
)
from project.api.v1.routers.grades.service import update_grade_relationships
from project.api.v1.routers.schema import FilterParams
from project.models import GradeStream, SubjectOffering
from project.models.grade import Grade
from project.models.year import Year
from project.schema.models import GradeWithRelatedSchema
from project.schema.models.grade_schema import GradeSchema
from project.utils.enum import PermissionEnum
from project.utils.utils import sort_grade_key

router = APIRouter(prefix="", tags=["Grades"])


@router.get(
    "/grades",
    response_model=List[GradeSchema],
)
async def get_grades(
    session: SessionDep,
    user_in: AuthenticatedRoute,
) -> Sequence[Grade]:
    """
    Returns specific academic year
    """
    if not user_in.has_permission(PermissionEnum.GRADES_READ):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to read grades.",
        )

    grades = (await session.execute(select(Grade))).scalars().all()

    sorted_grades = sorted(grades, key=sort_grade_key)

    return sorted_grades


@router.post(
    "/grades",
    response_model=NewGradeSuccess,
)
async def post_grade(
    session: SessionDep,
    new_grade: NewGrade,
    user_in: AuthenticatedRoute,
) -> Dict[str, Any]:
    """
    Creates a new Grade
    """
    if not user_in.has_permission(PermissionEnum.GRADES_WRITE):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to write grades.",
        )

    existing_grade_name = (
        await session.execute(
            select(Grade).where(
                Grade.grade == new_grade.grade,
                Grade.school_id == user_in.membership.school_id,
            )
        )
    ).first()

    if existing_grade_name:
        raise HTTPException(
            status_code=400,
            detail="Grade name for the school already exists.",
        )

    try:
        grade = Grade(
            school_id=user_in.membership.school_id,
            grade=new_grade.grade,
            level=new_grade.level,
            has_stream=new_grade.has_stream,
        )
        session.add(grade)
        await session.commit()
        await session.refresh(grade)

        return {"message": "Grade created Successfully", "id": grade.id}
    except Exception as e:
        logger.error(f"Error creating grade: {e}")
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Creation failed: {str(e)}")


@router.get(
    "/grade-offerings",
    response_model=List[GradeSetupSchema],
)
async def get_grade_offerings(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    query: Annotated[FilterParams, Query()],
) -> Sequence[Grade]:
    """
    Returns All Grades with in academic year
    """
    if not user_in.has_permission(PermissionEnum.GRADES_READ):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to read grades.",
        )

    year = await session.get(Year, query.year_id)
    if not year:
        raise HTTPException(status_code=404, detail="Academic year not found.")

    grade = (
        select(Grade)
        .join(Grade.grade_streams)
        .join(GradeStream.subject_offerings)
        .where(SubjectOffering.year_id == year.id)
    )

    if query.q:
        filter = re.sub(r"^gr?a?d?e? ?", "", query.q.strip(), flags=re.IGNORECASE)
        grade = grade.where(Grade.grade.ilike(f"%{filter}%"))

    grade_offering = (
        (
            await session.execute(
                grade.options(
                    # Grade -> Sections
                    selectinload(Grade.sections),
                    # Grade -> Streams
                    selectinload(Grade.grade_streams).selectinload(GradeStream.stream),
                    # Grade -> Stream -> Subjects
                    selectinload(Grade.grade_streams)
                    .selectinload(GradeStream.subject_offerings)
                    .selectinload(SubjectOffering.subject),
                ).group_by(Grade.id)
            )
        )
        .scalars()
        .all()
    )

    sorted_grades = sorted(grade_offering, key=sort_grade_key)

    return sorted_grades


@router.get(
    "/grade-offerings/{grade_id}",
    response_model=GradeSetupSchema,
)
async def get_grade_offerings_by_id(
    grade_id: uuid.UUID,
    session: SessionDep,
    user_in: AuthenticatedRoute,
) -> Grade:
    """
    Returns specific Grade SetUp
    """
    if not user_in.has_permission(PermissionEnum.GRADES_READ):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to read grades.",
        )

    grade_offering = (
        await session.execute(
            select(Grade)
            .where(Grade.id == grade_id)
            .options(
                selectinload(Grade.sections),
                selectinload(Grade.grade_streams).selectinload(GradeStream.stream),
                selectinload(Grade.grade_streams)
                .selectinload(GradeStream.subject_offerings)
                .selectinload(SubjectOffering.subject),
            )
            .group_by(Grade.id)
        )
    ).scalar_one_or_none()

    if not grade_offering:
        raise HTTPException(
            status_code=404,
            detail=f"Grade with ID {grade_id} not found.",
        )

    return grade_offering


@router.patch(
    "/grades/setup/{grade_id}",
    response_model=UpdateGradeSetupSuccess,
)
async def patch_grade_setup(
    session: SessionDep,
    grade_id: uuid.UUID,
    update_data: UpdateGradeSetup,
    user_in: AuthenticatedRoute,
) -> Dict[str, str]:
    """
    Updates specific Grade SetUp
    """
    grade = await session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(
            status_code=404,
            detail=f"Grade with ID {grade_id} not found.",
        )
    try:
        # Update simple fields
        for key in update_data.model_fields_set - {
            "subjects",
            "streams",
            "sections",
        }:
            if hasattr(grade, key):
                setattr(grade, key, getattr(update_data, key))

        # Update relationships
        await update_grade_relationships(
            year_id=uuid.UUID(),  # TODO: Pass actual year
            grade=grade,
            update_data=update_data,
            session=session,
        )

        await session.commit()

        return {"message": "Grade Setup Updated Successfully"}
    except IntegrityError as e:
        await session.rollback()
        if "uq_grade_stream_subject" in str(e.orig):
            raise HTTPException(
                status_code=422,
                detail="This subject already exists for the grade and stream.",
            )
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")
    except Exception as e:
        logger.error(f"Error updating grade setup: {e}")
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")


@router.get(
    "/grades/{grade_id}",
    response_model=GradeSchema,
)
async def get_grade_by_id(
    session: SessionDep,
    grade_id: uuid.UUID,
    user_in: AuthenticatedRoute,
) -> Grade:
    """
    Returns specific academic grade
    """
    if not user_in.has_permission(PermissionEnum.GRADES_READ):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to read grades.",
        )

    grade = await session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(
            status_code=404,
            detail=f"Grade with ID {grade_id} not found.",
        )

    return grade


@router.get(
    "/grades/{grade_id}/relation",
    response_model=GradeWithRelatedSchema,
)
async def get_grade_relation(
    session: SessionDep,
    grade_id: uuid.UUID,
    user_in: AuthenticatedRoute,
) -> Grade:
    """
    Returns specific academic grade
    """
    grade = (
        await session.execute(
            select(Grade)
            .where(Grade.id == grade_id)
            .options(
                selectinload(Grade.sections),
            )
        )
    ).scalar_one_or_none()

    if not grade:
        raise HTTPException(
            status_code=404,
            detail=f"Grade with ID {grade_id} not found.",
        )

    return grade
