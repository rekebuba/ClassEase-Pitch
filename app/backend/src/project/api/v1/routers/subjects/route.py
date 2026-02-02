import uuid
from typing import Annotated, Any, Dict, List, Sequence

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select

from project.api.v1.routers.dependencies import SessionDep, admin_route, shared_route
from project.api.v1.routers.schema import FilterParams
from project.api.v1.routers.subjects.schema import (
    NewSubject,
    NewSubjectSuccess,
    SubjectSetupSchema,
    UpdateSubjectSetup,
    UpdateSubjectSetupSuccess,
)
from project.api.v1.routers.subjects.service import update_subject_relationships
from project.models.subject import Subject
from project.models.year import Year
from project.schema.models.subject_schema import (
    SubjectSchema,
)

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.get(
    "/",
    response_model=List[SubjectSchema],
)
def get_subjects(
    session: SessionDep,
    query: Annotated[FilterParams, Query()],
    user_in: shared_route,
) -> Sequence[Subject]:
    """
    Returns All Subjects with in academic year
    """
    year = session.get(Year, query.year_id)
    if not year:
        raise HTTPException(
            status_code=404,
            detail=f"Year with ID {query.year_id} not found.",
        )

    subjects = session.scalars(
        select(Subject).where(Subject.year_id == query.year_id).order_by(Subject.name)
    ).all()

    return subjects


@router.post(
    "/",
    response_model=NewSubjectSuccess,
)
def post_subject(
    session: SessionDep,
    new_subject: NewSubject,
    user_in: admin_route,
) -> Dict[str, Any]:
    """
    Creates a new Subject
    """
    errors = {}

    existing_subject_name = session.scalars(
        select(Subject).where(
            Subject.name == new_subject.name,
            Subject.year_id == new_subject.year_id,
        )
    ).first()

    if existing_subject_name:
        errors["name"] = "Subject name for the year already exists."

    existing_subject_code = session.scalars(
        select(Subject).where(
            Subject.code == new_subject.code,
            Subject.year_id == new_subject.year_id,
        )
    ).first()
    if existing_subject_code:
        errors["code"] = "Subject code for the year already exists."

    if errors:
        raise HTTPException(status_code=400, detail=errors)

    try:
        subject = Subject(
            name=new_subject.name,
            code=new_subject.code,
            year_id=new_subject.year_id,
        )
        session.add(subject)
        session.commit()
        session.refresh(subject)

        return {"message": "Subject created Successfully", "id": subject.id}
    except Exception as e:
        print(f"Error creating subject: {e}")
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Creation failed: {str(e)}")


@router.get(
    "/setup",
    response_model=List[SubjectSetupSchema],
)
def get_subjects_setup(
    session: SessionDep,
    query: Annotated[FilterParams, Query()],
    user_in: shared_route,
) -> Sequence[Subject]:
    """
    Returns All Subjects with in academic year
    """
    year = session.get(Year, query.year_id)
    if not year:
        raise HTTPException(
            status_code=404,
            detail=f"Year with ID {query.year_id} not found.",
        )

    stmt = select(Subject).where(Subject.year_id == query.year_id)
    if query.q:
        stmt = stmt.where(Subject.name.ilike(f"%{query.q}%"))

    subjects = session.scalars(stmt.order_by(Subject.name)).all()

    return subjects


@router.get(
    "/setup/{subject_id}",
    response_model=SubjectSetupSchema,
)
def get_subject_setup_by_id(
    session: SessionDep,
    subject_id: uuid.UUID,
    user_in: shared_route,
) -> Subject:
    """
    Returns specific academic subject
    """
    subject = session.get(Subject, subject_id)
    if not subject:
        raise HTTPException(
            status_code=404,
            detail=f"Subject with ID {subject_id} not found.",
        )

    return subject


@router.patch(
    "/setup/{subject_id}",
    response_model=UpdateSubjectSetupSuccess,
)
def patch_subject_setup(
    session: SessionDep,
    subject_id: uuid.UUID,
    update_data: UpdateSubjectSetup,
    user_in: admin_route,
) -> Dict[str, str]:
    """
    Updates Subject SetUp
    """
    subject = session.get(Subject, subject_id)
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
        update_subject_relationships(subject, update_data, session)

        session.commit()

        return {"message": "Subject Setup Updated Successfully"}
    except Exception as e:
        print(f"Error updating grade setup: {e}")
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")


@router.get(
    "/{subject_id}",
    response_model=SubjectSchema,
)
def get_subject_by_id(
    session: SessionDep,
    subject_id: uuid.UUID,
    user_in: shared_route,
) -> Subject:
    """
    Returns specific academic subject
    """
    subject = session.get(Subject, subject_id)
    if not subject:
        raise HTTPException(
            status_code=404,
            detail=f"Subject with ID {subject_id} not found.",
        )

    return subject
