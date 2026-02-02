from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Query

from project.api.v1.routers.dependencies import SessionDep, admin_route
from project.api.v1.routers.schema import FilterParams
from project.models.academic_term import AcademicTerm
from project.models.year import Year
from project.schema.models.academic_term_schema import AcademicTermSchema

router = APIRouter(prefix="/terms", tags=["Academic Terms"])


@router.get("/", response_model=List[AcademicTermSchema])
def get_academic_terms(
    session: SessionDep,
    query: Annotated[FilterParams, Query()],
    user_in: admin_route,
) -> List[AcademicTerm]:
    """This endpoint will return a list of academic terms for a given year."""
    year = session.get(Year, query.year_id)
    if not year:
        raise HTTPException(
            status_code=404,
            detail=f"Year with ID {query.year_id} not found.",
        )

    terms = (
        session.query(AcademicTerm)
        .filter(AcademicTerm.year_id == year.id)
        .order_by(AcademicTerm.name)
        .all()
    )

    return terms
