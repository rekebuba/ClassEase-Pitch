from typing import Annotated, List, Sequence

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import (
    joinedload,
    with_loader_criteria,
)

from project.api.v1.routers.dependencies import SessionDep, admin_route
from project.api.v1.routers.teachers.schema import (
    AssignTeacher,
    TeacherBasicInfo,
    TeachersQuery,
)
from project.models.academic_term import AcademicTerm
from project.models.employee import Employee
from project.models.grade import Grade
from project.models.grade_stream_subject import GradeStreamSubject
from project.models.section import Section
from project.models.stream import Stream
from project.models.teacher_record import TeacherRecord
from project.models.teacher_record_link import TeacherRecordLink
from project.models.year import Year
from project.schema.schema import SuccessResponseSchema
from project.utils.enum import EmployeePositionEnum

router = APIRouter(prefix="/teachers", tags=["Teachers"])


@router.get("/", response_model=List[TeacherBasicInfo])
def get_teachers(
    session: SessionDep,
    user_in: admin_route,
    q: Annotated[TeachersQuery, Query()],
) -> Sequence[Employee]:
    """This endpoint will return employees based on the provided filters."""
    if session.query(Year).where(Year.id == q.year_id).first() is None:
        raise HTTPException(
            status_code=400,
            detail=f"Year with ID {q.year_id} not found.",
        )

    if (
        session.query(AcademicTerm).where(AcademicTerm.id == q.academic_term_id).first()
        is None
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Academic Term with ID {q.academic_term_id} not found.",
        )

    filtered_gss_subquery = (
        select(GradeStreamSubject.id)
        .join(
            TeacherRecord,
            TeacherRecord.grade_stream_subject_id == GradeStreamSubject.id,
        )
        .join(
            TeacherRecordLink, TeacherRecordLink.teacher_record_id == TeacherRecord.id
        )
        .where(TeacherRecordLink.section_id == Section.id)
        .correlate(Grade)
        .scalar_subquery()
    )

    teachers = select(Employee).options(
        with_loader_criteria(Section, Section.id == TeacherRecordLink.section_id),
        with_loader_criteria(
            GradeStreamSubject, GradeStreamSubject.id.in_(filtered_gss_subquery)
        ),
        with_loader_criteria(Year, Year.id == q.year_id),
        with_loader_criteria(AcademicTerm, AcademicTerm.id == q.academic_term_id),
        joinedload(Employee.teacher_records).joinedload(TeacherRecord.academic_term),
        joinedload(Employee.teacher_records)
        .joinedload(TeacherRecord.grade_stream_subject)
        .joinedload(GradeStreamSubject.subject),
        joinedload(Employee.teacher_records)
        .joinedload(TeacherRecord.grade_stream_subject)
        .joinedload(GradeStreamSubject.stream),
    )

    result = session.scalars(teachers).unique().all()

    return result


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
        existing_record = session.scalar(
            select(TeacherRecord).where(
                TeacherRecord.employee_id == assign_data.teacher_id,
                TeacherRecord.academic_term_id == term_id,
                TeacherRecord.grade_stream_subject_id == gss.id,
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
        )

        session.add(new_record)
        session.flush()

        for section in assign_data.grade.sections:
            session_exists = session.get(Section, section.id)
            if not session_exists:
                raise HTTPException(
                    status_code=400,
                    detail=f"Section with ID {section.id} not found.",
                )

            teacher_record_link_exists = session.scalar(
                select(TeacherRecordLink).where(
                    TeacherRecordLink.teacher_record_id == new_record.id,
                    TeacherRecordLink.section_id == section.id,
                )
            )
            if teacher_record_link_exists:
                raise HTTPException(
                    status_code=400,
                    detail=f"Teacher is already assigned to section with ID \
                         {section.id}.",
                )

            session.add(
                TeacherRecordLink(
                    teacher_record_id=new_record.id, section_id=section.id
                )
            )

    session.add(new_record)
    session.commit()

    return SuccessResponseSchema(message="Teacher assigned successfully.")
