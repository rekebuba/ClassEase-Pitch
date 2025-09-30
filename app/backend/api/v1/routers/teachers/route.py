from typing import Annotated, List, Optional, Sequence
import uuid

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy import and_, cast, func, select
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import (
    with_loader_criteria,
    selectinload,
    contains_eager,
    joinedload,
)
from api.v1.routers.dependencies import SessionDep, admin_route
from api.v1.routers.teachers.schema import (
    AssignTeacher,
    TeacherBasicInfo,
)
from models.academic_term import AcademicTerm
from models.employee import Employee
from models.grade import Grade
from models.grade_stream_subject import GradeStreamSubject
from models.section import Section
from models.stream import Stream
from models.subject import Subject
from models.teacher_record import TeacherRecord
from models.teacher_record_link import TeacherRecordLink
from schema.models.academic_term_schema import AcademicTermSchema
from schema.models.grade_schema import GradeSchema
from schema.models.section_schema import SectionSchema
from schema.models.subject_schema import SubjectSchema
from schema.schema import SuccessResponseSchema
from utils.enum import AcademicTermEnum, EmployeePositionEnum
from utils.utils import to_camel

router = APIRouter(prefix="/teachers", tags=["Teachers"])


class TestSchemaSection(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    grade_id: uuid.UUID
    section: str
    teacher_subjects: List[SubjectSchema]


class TestGSS(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    grade: str
    sections: List[TestSchemaSection]
    subjects: List[SubjectSchema]


class TestTeacherRecord(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    academic_term: AcademicTermSchema
    academic_term_id: uuid.UUID
    name: AcademicTermEnum
    # grade: TestGSS


class TestSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    teacher_records: List[TestTeacherRecord]


@router.get("/", response_model=List[TeacherBasicInfo])
def get_teachers(
    session: SessionDep,
    user_in: admin_route,
    q: Annotated[Optional[str], Query()] = None,
) -> Sequence[Employee]:
    """This endpoint will return employees based on the provided filters."""

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
                    detail=f"Teacher is already assigned to section with ID {section.id}.",
                )

            session.add(
                TeacherRecordLink(
                    teacher_record_id=new_record.id, section_id=section.id
                )
            )

    session.add(new_record)
    session.commit()

    return SuccessResponseSchema(message="Teacher assigned successfully.")
