import re
import uuid
from typing import Annotated, Any, Dict, List, Sequence

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from api.v1.routers.dependencies import SessionDep, admin_route, shared_route
from api.v1.routers.grades.schema import (
    GradeSetupSchema,
    NewGrade,
    NewGradeSuccess,
    UpdateGradeSetup,
    UpdateGradeSetupSuccess,
)
from api.v1.routers.grades.service import update_grade_relationships
from api.v1.routers.schema import FilterParams
from models.grade import Grade
from models.year import Year
from schema.models.grade_schema import GradeSchema
from utils.utils import sort_grade_key

router = APIRouter(prefix="/grades", tags=["Grades"])


@router.get(
    "/",
    response_model=List[GradeSchema],
)
def get_grades(
    session: SessionDep,
    query: Annotated[FilterParams, Query()],
    user_in: shared_route,
) -> Sequence[Grade]:
    """
    Returns specific academic year
    """
    year = session.get(Year, query.year_id)
    if not year:
        raise HTTPException(
            status_code=404,
            detail=f"Year with ID {query.year_id} not found.",
        )

    grades = session.scalars(select(Grade).where(Grade.year_id == query.year_id)).all()

    sorted_grades = sorted(grades, key=sort_grade_key)

    return sorted_grades


@router.post(
    "/",
    response_model=NewGradeSuccess,
)
def post_grade(
    session: SessionDep,
    new_grade: NewGrade,
    user_in: admin_route,
) -> Dict[str, Any]:
    """
    Creates a new Grade
    """
    errors = {}

    existing_grade_name = session.scalars(
        select(Grade).where(
            Grade.grade == new_grade.grade,
            Grade.year_id == new_grade.year_id,
        )
    ).first()

    if existing_grade_name:
        errors["grade"] = "Grade name for the year already exists."

    if errors:
        raise HTTPException(status_code=400, detail=errors)

    try:
        grade = Grade(
            grade=new_grade.grade,
            level=new_grade.level,
            has_stream=new_grade.has_stream,
            year_id=new_grade.year_id,
        )
        session.add(grade)
        session.commit()
        session.refresh(grade)

        return {"message": "Grade created Successfully", "id": grade.id}
    except Exception as e:
        print(f"Error creating grade: {e}")
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Creation failed: {str(e)}")


@router.get(
    "/setup",
    response_model=List[GradeSetupSchema],
)
def get_grades_setup(
    query: Annotated[FilterParams, Query()],
    session: SessionDep,
    user_in: shared_route,
) -> Sequence[Grade]:
    """
    Returns specific academic year
    """
    year = session.get(Year, query.year_id)
    if not year:
        raise HTTPException(
            status_code=404,
            detail=f"Year with ID {query.year_id} not found.",
        )

    stmt = select(Grade).where(Grade.year_id == query.year_id)
    if query.q:
        filter = re.sub(r"^gr?a?d?e? ?", "", query.q.strip(), flags=re.IGNORECASE)
        stmt = stmt.where(Grade.grade.ilike(f"%{filter}%"))

    grades = session.scalars(stmt).all()

    sorted_grades = sorted(grades, key=sort_grade_key)

    return sorted_grades


@router.get(
    "/setup/{grade_id}",
    response_model=GradeSetupSchema,
)
def get_grades_setup_by_id(
    grade_id: uuid.UUID,
    session: SessionDep,
    user_in: shared_route,
) -> Grade:
    """
    Returns specific Grade SetUp
    """

    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(
            status_code=404,
            detail=f"Grade with ID {grade_id} not found.",
        )

    return grade


@router.patch(
    "/setup/{grade_id}",
    response_model=UpdateGradeSetupSuccess,
)
def patch_grade_setup(
    session: SessionDep,
    grade_id: uuid.UUID,
    update_data: UpdateGradeSetup,
    user_in: admin_route,
) -> Dict[str, str]:
    """
    Updates specific Grade SetUp
    """
    grade = session.get(Grade, grade_id)
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
        update_grade_relationships(grade, update_data, session)

        session.commit()

        return {"message": "Grade Setup Updated Successfully"}
    except IntegrityError as e:
        session.rollback()
        if "uq_grade_stream_subject" in str(e.orig):
            raise HTTPException(
                status_code=422,
                detail="This subject already exists for the grade and stream.",
            )
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")
    except Exception as e:
        print(f"Error updating grade setup: {e}")
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")


@router.get(
    "/{grade_id}",
    response_model=GradeSchema,
)
def get_grade_by_id(
    session: SessionDep,
    grade_id: uuid.UUID,
    user_in: shared_route,
) -> Grade:
    """
    Returns specific academic grade
    """
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(
            status_code=404,
            detail=f"Grade with ID {grade_id} not found.",
        )

    return grade
