import uuid
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from project.models.academic_term import AcademicTerm
from project.utils.enum import AcademicTermEnum, AcademicTermTypeEnum


def create_academic_term(
    *,
    year_id: uuid.UUID,
    school_id: uuid.UUID,
    calendar_type: AcademicTermTypeEnum,
    session: AsyncSession,
) -> None:
    """
    Creates academic terms for a new academic year based on its calendar type.
    """
    num_terms = 2 if calendar_type == AcademicTermTypeEnum.SEMESTER else 4

    term_names = [enum for enum in AcademicTermEnum][:num_terms]

    terms_to_create = [
        AcademicTerm(
            school_id=school_id,
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
