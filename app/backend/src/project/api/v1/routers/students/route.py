import uuid
from typing import Annotated, List, Sequence

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from starlette import status

from project.api.v1.routers.dependencies import (
    AuthenticatedRoute,
    PlatformAuthenticatedRoute,
    SessionDep,
)
from project.api.v1.routers.schema import FilterParams
from project.api.v1.routers.school.schema import (
    StudentProfile,
)
from project.api.v1.routers.students.schema import (
    EnrollmentApplicationPost,
    EnrollmentOpportunityPost,
    EnrollmentOpportunitySchema,
    EnrollStudent,
    EnrollStudentApplication,
    StudentBasicInfo,
    UpdateStudentStatus,
)
from project.core.access_control import (
    ensure_membership_role,
    provision_user_membership,
)
from project.models import (
    AcademicTerm,
    ApplicationAcademicBackground,
    ApplicationAddress,
    ApplicationHealthRecord,
    EnrollmentApplication,
    EnrollmentOpportunity,
    Role,
    SchoolMembership,
    Student,
    StudentAcademicBackground,
    StudentAddress,
    StudentEnrollment,
    StudentHealthRecord,
    StudentTermRecord,
    StudentYearRecord,
    User,
    UserGuardian,
)
from project.models.grade import Grade
from project.models.year import Year
from project.schema.schema import SuccessResponse, SuccessResponseSchema
from project.utils.enum import (
    EnrollmentApplicationStatusEnum,
    MfaStateEnum,
    PermissionEnum,
    RoleEnum,
    SchoolMembershipStatusEnum,
    StudentApplicationStatusEnum,
)
from project.utils.utils import generate_id

router = APIRouter()


@router.post(
    "/enrollment-opportunities",
    status_code=status.HTTP_201_CREATED,
    tags=["Student-Enrollments"],
    response_model=SuccessResponse,
)
async def post_student_enrollment_opportunity(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    student_enrollment: EnrollmentOpportunityPost,
) -> SuccessResponse:
    """Creates a new student enrollment opportunity."""
    if not user_in.has_permission(PermissionEnum.STUDENTS_WRITE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    # EnrollmentOpportunity
    enrollment_opportunity = EnrollmentOpportunity(
        school_id=user_in.membership.school_id,
        academic_year_id=student_enrollment.academic_year_id,
        grade_id=student_enrollment.grade_id,
        application_deadline=student_enrollment.application_deadline,
        capacity=student_enrollment.capacity,
        allow_applications=student_enrollment.allow_applications,
    )

    session.add(enrollment_opportunity)
    await session.commit()

    return SuccessResponse(id=enrollment_opportunity.id, message="Student Enrollment Opportunity Created Successfully")


@router.get(
    "/enrollment-opportunities",
    response_model=List[EnrollmentOpportunitySchema],
    tags=["Student-Enrollments"],
)
async def get_student_enrollment_opportunities(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    q: Annotated[FilterParams, Query()],
) -> Sequence[EnrollmentOpportunity]:
    """Returns all student enrollment opportunities."""
    if not user_in.has_permission(PermissionEnum.STUDENTS_READ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    enrollment_opportunities = (
        (
            await session.execute(
                select(EnrollmentOpportunity)
                .options(
                    selectinload(EnrollmentOpportunity.academic_year),
                    selectinload(EnrollmentOpportunity.grade),
                )
                .where(
                    EnrollmentOpportunity.school_id == user_in.membership.school_id,
                    EnrollmentOpportunity.academic_year_id == q.year_id,
                )
            )
        )
        .scalars()
        .all()
    )

    return enrollment_opportunities


@router.post(
    "/enrollment-applications",
    status_code=status.HTTP_201_CREATED,
    tags=["Student-Enrollments"],
    response_model=SuccessResponse,
)
async def post_student_enrollment(
    session: SessionDep,
    user_in: PlatformAuthenticatedRoute,
    enrollment_app: EnrollmentApplicationPost,
) -> SuccessResponse:
    """Enrolls a student in the system."""

    enrollment_opportunity = await session.scalar(
        select(EnrollmentOpportunity).where(EnrollmentOpportunity.id == enrollment_app.opportunity_id)
    )

    if not enrollment_opportunity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enrollment Opportunity with ID {enrollment_app.opportunity_id} not found.",
        )

    student_user = None
    if enrollment_app.student_user_id:
        student_user = await session.scalar(select(User).where(User.id == enrollment_app.student_user_id))

    # Create temporary/unverified user if not existing
    if not student_user and enrollment_app.user:
        student_user = User(
            first_name=enrollment_app.user.first_name,
            father_name=enrollment_app.user.father_name,
            grand_father_name=enrollment_app.user.grand_father_name,
            date_of_birth=enrollment_app.user.date_of_birth,
            gender=enrollment_app.user.gender,
            email=enrollment_app.user.email,
            phone=enrollment_app.user.phone,
            is_active=False,
            is_verified=False,
        )
        session.add(student_user)
        await session.flush()

    if not student_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student user could not be found or created.",
        )

    application = EnrollmentApplication(
        school_id=enrollment_opportunity.school_id,
        applicant_user_id=user_in.user.id,
        student_user_id=student_user.id,
        opportunity_id=enrollment_app.opportunity_id,
        applicant_note=enrollment_app.applicant_note,
        status=EnrollmentApplicationStatusEnum.PENDING,
    )

    # Establish guardian link if applicant is distinct from student
    if application.applicant_user_id != application.student_user_id:
        session.add(
            UserGuardian(
                guardian_user_id=application.applicant_user_id,
                dependent_user_id=application.student_user_id,
                relation=enrollment_app.relation or "",
            )
        )

    session.add(application)
    await session.flush()

    if enrollment_app.health_record:
        session.add(
            ApplicationHealthRecord(
                application_id=application.id,
                school_id=application.school_id,
                blood_type=enrollment_app.health_record.blood_type,
                has_disability=enrollment_app.health_record.has_disability,
                disability_details=enrollment_app.health_record.disability_details,
                has_medical_condition=enrollment_app.health_record.has_medical_condition,
                medical_details=enrollment_app.health_record.medical_details,
            )
        )

    if enrollment_app.academic_background:
        session.add(
            ApplicationAcademicBackground(
                application_id=application.id,
                school_id=application.school_id,
                previous_school=enrollment_app.academic_background.previous_school,
                is_transfer=enrollment_app.academic_background.is_transfer,
            )
        )

    if enrollment_app.address:
        session.add(
            ApplicationAddress(
                application_id=application.id,
                school_id=application.school_id,
                city=enrollment_app.address.city,
                state=enrollment_app.address.state,
                postal_code=enrollment_app.address.postal_code,
                nationality=enrollment_app.address.nationality,
                transportation=enrollment_app.address.transportation,
            )
        )

    await session.commit()

    return SuccessResponse(id=application.id, message="Student Application submitted successfully.")


@router.post(
    "/enrollment-applications/approve",
    status_code=status.HTTP_200_OK,
    tags=["Student-Enrollments"],
    response_model=SuccessResponse,
)
async def approve_student_enrollment(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    application_form: EnrollStudentApplication,
) -> SuccessResponse:
    """Approves a student enrollment application."""
    if not user_in.has_permission(PermissionEnum.STUDENTS_WRITE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    application = await session.scalar(
        select(EnrollmentApplication)
        .options(
            selectinload(EnrollmentApplication.health_record),
            selectinload(EnrollmentApplication.academic_background),
            selectinload(EnrollmentApplication.address),
        )
        .where(EnrollmentApplication.id == application_form.application_id)
    )

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enrollment Application with ID {application_form.application_id} not found.",
        )

    if application.school_id != user_in.membership.school_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to approve applications for this school.",
        )

    # Guard: Prevent double-approval
    if application.status == EnrollmentApplicationStatusEnum.ACCEPTED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This application has already been approved.",
        )

    # Guarantee SchoolMembership exists (Satisfies fk_students_membership_school)
    membership = await session.scalar(
        select(SchoolMembership).where(
            SchoolMembership.user_id == application.student_user_id,
            SchoolMembership.school_id == application.school_id,
        )
    )
    if not membership:
        membership = SchoolMembership(
            user_id=application.student_user_id,
            school_id=user_in.membership.school_id,
            status=SchoolMembershipStatusEnum.ACTIVE,
            mfa_state=MfaStateEnum.ENROLLED,
            is_primary=True,
            permissions_version=1,
        )

        session.add(membership)
        await session.flush()

    # Activate Student User account if dormant
    student_user = await session.scalar(select(User).where(User.id == application.student_user_id))
    if student_user and not student_user.is_active:
        student_user.is_active = True

    # Create Student profile
    student = Student(
        school_id=application.school_id,
        user_id=application.student_user_id,
        status=StudentApplicationStatusEnum.ACTIVE,
    )
    session.add(student)
    await session.flush()

    # Copy 1:1 Staging tables -> Active Extension tables
    if application.health_record:
        session.add(
            StudentHealthRecord(
                student_id=student.id,
                school_id=application.school_id,
                blood_type=application.health_record.blood_type,
                has_disability=application.health_record.has_disability,
                disability_details=application.health_record.disability_details,
                has_medical_condition=application.health_record.has_medical_condition,
                medical_details=application.health_record.medical_details,
            )
        )

    if application.academic_background:
        session.add(
            StudentAcademicBackground(
                student_id=student.id,
                school_id=application.school_id,
                previous_school=application.academic_background.previous_school,
                is_transfer=application.academic_background.is_transfer,
            )
        )

    if application.address:
        session.add(
            StudentAddress(
                student_id=student.id,
                school_id=application.school_id,
                city=application.address.city,
                state=application.address.state,
                postal_code=application.address.postal_code,
                nationality=application.address.nationality,
                transportation=application.address.transportation,
            )
        )

    # Mark application as accepted
    application.status = EnrollmentApplicationStatusEnum.ACCEPTED
    await session.commit()

    return SuccessResponse(
        id=student.id,
        message="Student enrollment application approved successfully.",
    )


@router.post(
    "/students",
    status_code=status.HTTP_201_CREATED,
    tags=["Students"],
    response_model=SuccessResponse,
)
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
    )

    session.add(
        UserGuardian(
            guardian_user_id=new_student.id,
            dependent_user_id=new_student.id,
            relation="",
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
