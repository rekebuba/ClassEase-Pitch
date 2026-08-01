import uuid
from typing import Annotated, List, Sequence

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from starlette import status

from project.api.v1.routers.dependencies import (
    AuthenticatedRoute,
    SessionDep,
)
from project.api.v1.routers.schema import FilterParams
from project.api.v1.routers.school.schema import (
    StudentProfile,
)
from project.api.v1.routers.students.schema import (
    EnrollStudent,
    StudentBasicInfo,
    UpdateStudentStatus,
)
from project.core.access_control import (
    ensure_membership_role,
    provision_user_membership,
)
from project.models import (
    AcademicTerm,
    Parent,
    ParentStudentLink,
    Role,
    SchoolMembership,
    Student,
    StudentEnrollment,
    StudentTermRecord,
    StudentYearRecord,
    User,
)
from project.models.grade import Grade
from project.models.year import Year
from project.schema.schema import SuccessResponse, SuccessResponseSchema
from project.utils.enum import (
    MfaStateEnum,
    PermissionEnum,
    RoleEnum,
    StudentApplicationStatusEnum,
)
from project.utils.utils import generate_id

router = APIRouter()


@router.post("/students", status_code=status.HTTP_201_CREATED)
async def student(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    student_data: StudentProfile,
) -> SuccessResponse:
    """Registers a new student in the system."""
    if not user_in.has_permission(PermissionEnum.STUDENTS_WRITE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    user = (
        await session.execute(
            select(User).where(User.id == student_data.user_id).options(selectinload(User.memberships))
        )
    ).scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User Not Found",
        )

    if not user.memberships:
        membership = SchoolMembership(
            school_id=user_in.membership.school_id,
            user_id=student_data.user_id,
        )

        session.add(membership)
        await session.flush()

        role = (await session.execute(select(Role).where(Role.name == RoleEnum.STUDENT))).scalar_one_or_none()

        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

        await ensure_membership_role(
            session,
            membership,
            role,
            user_in.membership.school_id,
        )

    new_student = Student(
        school_id=user_in.membership.school_id,
        user_id=user.id,
        city=student_data.city,
        state=student_data.state,
        postal_code=student_data.postal_code,
        nationality=student_data.nationality,
        blood_type=student_data.blood_type,
        previous_school=student_data.previous_school,
        transportation=student_data.transportation,
        has_medical_condition=student_data.has_medical_condition,
        medical_details=student_data.medical_details,
        has_disability=student_data.has_disability,
        disability_details=student_data.disability_details,
        is_transfer=student_data.is_transfer,
    )

    for parent in student_data.parents:
        new_parent = Parent(
            school_id=user_in.membership.school_id,
            user_id=user.id,
            relation=parent.relation,
            emergency_contact_phone=parent.emergency_contact_phone,
        )
        session.add(new_parent)
        await session.flush()

        session.add(
            ParentStudentLink(
                parent_user_id=new_parent.id,
                student_user_id=new_student.id,
            )
        )

    await session.commit()

    return SuccessResponse(id=new_student.id, message="Student Registered Successfully")


@router.get("/students", response_model=List[StudentBasicInfo])
async def get_students(
    session: SessionDep,
    query: Annotated[FilterParams, Query()],
    user_in: AuthenticatedRoute,
) -> Sequence[Student]:
    """This endpoint will return students based on the provided filters."""
    year = await session.get(Year, query.year_id)
    if not year:
        raise HTTPException(
            status_code=404,
            detail=f"Year with ID {query.year_id} not found.",
        )

    stm = select(Student).options(selectinload(Student.membership).selectinload(SchoolMembership.user))

    if query.q:
        stm = stm.where(Student.membership.user.first_name.ilike(f"%{query.q}%"))

    students = (await session.execute(stm)).scalars().all()

    return students


@router.get("/students/{student_id}", response_model=StudentBasicInfo)
async def get_student(
    session: SessionDep,
    student_id: uuid.UUID,
    user_in: AuthenticatedRoute,
) -> Student:
    """This endpoint will return a student based on the provided ID."""
    student = await session.get(Student, student_id)
    if not student:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} not found.",
        )
    return student


@router.delete("/students", response_model=SuccessResponseSchema)
async def delete_students(
    session: SessionDep,
    student_ids: Annotated[List[uuid.UUID], Query()],
    user_in: AuthenticatedRoute,
) -> SuccessResponseSchema:
    """This endpoint will delete students based on the provided IDs."""
    for student_id in student_ids:
        student = await session.get(Student, student_id)
        if not student:
            raise HTTPException(
                status_code=404,
                detail=f"Student with ID {student_id} not found.",
            )
        await session.delete(student)
    await session.commit()
    return SuccessResponseSchema(message="Students deleted successfully.")


@router.post("/students/enroll", status_code=status.HTTP_201_CREATED)
async def enroll_student(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    student: EnrollStudent,
) -> SuccessResponse:
    """Enrolls a student in the system."""
    if not user_in.has_permission(PermissionEnum.STUDENTS_WRITE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    new_student = StudentEnrollment(
        school_id=user_in.membership.school_id,
        student_id=student.student_id,
        year_id=student.year_id,
        class_section_id=student.class_section_id,
    )
    session.add(new_student)
    session.flush()

    stud_year_record = StudentYearRecord(
        school_id=user_in.membership.school_id,
        student_enrollment_id=new_student.id,
        average=None,
        rank=None,
        promotion_status=None,
    )

    terms = (await session.execute(select(AcademicTerm).where(AcademicTerm.year_id == student.year_id))).all()

    for term in terms:
        stud_term_record = StudentTermRecord(
            school_id=user_in.membership.school_id,
            student_enrollment_id=new_student.id,
            student_year_record_id=stud_year_record.id,
            academic_term_id=term.id,
            average=None,
            rank=None,
            pass_status=None,
            teacher_remarks=None,
        )
        session.add(stud_term_record)

    await session.commit()
    return SuccessResponse(id=new_student.id, message="Student enrolled successfully.")


@router.patch("/students/status", response_model=SuccessResponseSchema)
async def update_student_status(
    session: SessionDep,
    students: UpdateStudentStatus,
    user_in: AuthenticatedRoute,
) -> SuccessResponseSchema:
    """This endpoint will patch students based on the provided IDs."""
    for student_id in students.student_ids:
        student = await session.get(Student, student_id)
        if not student:
            raise HTTPException(
                status_code=404,
                detail=f"Student with ID {student_id} not found.",
            )

        student.status = students.status

        if students.status == StudentApplicationStatusEnum.ACTIVE and student.user_id is None:
            year = (
                await session.execute(
                    select(Year)
                    .join(Grade, Grade.year_id == Year.id)
                    .where(Grade.id == student.registered_for_grade_id)
                )
            ).scalar_one_or_none()
            if year is None:
                raise HTTPException(
                    status_code=404,
                    detail="No academic year found for the student.",
                )
            username = await generate_id(
                session=session,
                role=RoleEnum.STUDENT,
                year=year,
            )
            new_user, membership = await provision_user_membership(
                session,
                school=user_in.membership.school,
                membership_role_name=RoleEnum.STUDENT,
                login_identifier=username,
                password=username,
                email=None,
                phone=None,
                is_active=True,
                is_verified=False,
                mfa_state=MfaStateEnum.NOT_ENROLLED,
            )
            student.user_id = new_user.id
            student.school_membership_id = membership.id
            student.school_id = membership.school_id

    await session.commit()

    return SuccessResponseSchema(
        message=f"Student{'s' if len(students.student_ids) > 1 else ''} Status \
            Updated successfully."
    )
