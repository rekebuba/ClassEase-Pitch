from typing import Annotated, List, Optional, Sequence

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select

from api.v1.routers.dependencies import SessionDep, admin_route
from api.v1.routers.teachers.schema import (
    AssignTeacher,
    TeacherBasicInfo,
)
from models.academic_term import AcademicTerm
from models.employee import Employee
from models.grade import Grade
from models.grade_stream_subject import GradeStreamSubject
from models.stream import Stream
from models.teacher_record import TeacherRecord
from schema.schema import SuccessResponseSchema
from utils.enum import EmployeePositionEnum

router = APIRouter(prefix="/teachers", tags=["Teachers"])


@router.get("/", response_model=List[TeacherBasicInfo])
def get_teachers(
    session: SessionDep,
    user_in: admin_route,
    q: Annotated[Optional[str], Query()] = None,
) -> Sequence[Employee]:
    """This endpoint will return employees based on the provided filters."""
    stm = select(Employee).where(
        Employee.position == EmployeePositionEnum.TEACHING_STAFF
    )

    if q:
        stm = stm.where(Employee.first_name.ilike(f"%{q}%"))

    employees = session.scalars(stm).all()

    return employees


@router.post("/", response_model=SuccessResponseSchema)
def assign_teacher(
    session: SessionDep,
    assign_data: AssignTeacher,
    user_in: admin_route,
) -> SuccessResponseSchema:
    """
    This endpoint will assign a teacher to
        - academic term
        - grade stream subject
        - section
    """
    teacher = session.get(Employee, assign_data.teacher_id)

    if not teacher:
        raise HTTPException(
            status_code=400,
            detail=f"Teacher with ID {assign_data.teacher_id} not found.",
        )

    if teacher.position != EmployeePositionEnum.TEACHING_STAFF:
        raise HTTPException(
            status_code=400,
            detail=f"Employee with ID {assign_data.teacher_id} is not a teacher.",
        )

    grade = session.scalar(select(Grade).where(Grade.id == assign_data.grade.id))
    if not grade:
        raise HTTPException(
            status_code=400,
            detail=f"Grade with ID {assign_data.grade.id} not found.",
        )

    if grade and grade.has_stream:
        if not assign_data.grade.stream_id:
            raise HTTPException(
                status_code=400,
                detail="Stream ID is required for the selected grade.",
            )

        stream = session.scalar(
            select(Stream)
            .where(Stream.id == assign_data.grade.stream_id)
            .where(Stream.grade_id == assign_data.grade.id)
        )
        if not stream:
            raise HTTPException(
                status_code=400,
                detail=f"Stream with ID {assign_data.grade.stream_id} not found.",
            )

    gss = session.scalar(
        select(GradeStreamSubject)
        .where(GradeStreamSubject.stream_id == assign_data.grade.stream_id)
        .where(GradeStreamSubject.subject_id == assign_data.subject_id)
        .where(GradeStreamSubject.grade_id == assign_data.grade.id)
    )

    if not gss:
        raise HTTPException(
            status_code=404,
            detail="Grade Stream Subject not found \
                for the given stream, subject, and grade.",
        )
    term_ids = session.scalars(
        select(AcademicTerm.id).where(AcademicTerm.year_id == assign_data.year_id)
    )
    if not term_ids:
        raise HTTPException(
            status_code=404,
            detail=f"Academic Term with Year ID {assign_data.year_id} not found.",
        )

    for term_id in term_ids:
        for section in assign_data.grade.sections:
            existing_record = session.scalar(
                select(TeacherRecord).where(
                    TeacherRecord.employee_id == assign_data.teacher_id,
                    TeacherRecord.academic_term_id == term_id,
                    TeacherRecord.grade_stream_subject_id == gss.id,
                    TeacherRecord.section_id == section.id,
                )
            )

            if existing_record:
                raise HTTPException(
                    status_code=400,
                    detail="Another Teacher is already assigned with the same details.",
                )

            new_record = TeacherRecord(
                employee_id=assign_data.teacher_id,
                academic_term_id=term_id,
                grade_stream_subject_id=gss.id,
                section_id=section.id,
            )

            session.add(new_record)

    session.add(new_record)
    session.commit()

    return SuccessResponseSchema(message="Teacher assigned successfully.")
