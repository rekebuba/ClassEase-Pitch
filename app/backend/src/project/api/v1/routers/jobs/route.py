import uuid
from typing import Annotated, List, Optional, Sequence

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from project.api.v1.routers.dependencies import (
    AuthenticatedRoute,
    PlatformAuthenticatedRoute,
    SessionDep,
)
from project.api.v1.routers.jobs.schema import HireJobApplication, JobApplicationPost, JobPost
from project.core.access_control import ensure_membership_role
from project.models import (
    Employee,
    EmployeePosition,
    EmploymentApplication,
    EmploymentContract,
    JobPosting,
    Position,
    Role,
    SchoolMembership,
    TeacherProfile,
    User,
)
from project.schema.models import EmploymentApplicationSchema
from project.schema.models.job_schema import JobSchema
from project.schema.schema import SuccessResponse
from project.utils.enum import ContractStatusEnum, EmploymentApplicationStatusEnum, PermissionEnum, RoleEnum

router = APIRouter()


@router.post(
    "/jobs",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponse,
    tags=["Jobs"],
)
async def post_job(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    data: JobPost,
) -> SuccessResponse:
    """Registers a new job post in the system."""
    if not user_in.has_permission(PermissionEnum.EMPLOYEES_WRITE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )
    job = JobPosting(
        school_id=user_in.membership.school_id,
        position_id=data.position_id,
        description=data.description,
        employment_type=data.employment_type,
        application_deadline=data.application_deadline,
        openings_count=data.openings_count,
    )

    session.add(job)
    await session.commit()

    return SuccessResponse(id=job.id, message="Job post registered successfully")


@router.get(
    "/school-jobs",
    status_code=status.HTTP_200_OK,
    response_model=List[JobSchema],
    tags=["Jobs"],
)
async def get_school_jobs(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    q: Annotated[Optional[str], Query()] = None,
) -> Sequence[JobPosting]:
    """This endpoint will return job postings based on the provided filters."""
    stm = select(JobPosting).where(JobPosting.school_id == user_in.membership.school_id)

    if q:
        stm = stm.where(JobPosting.description.ilike(f"%{q}%"))

    jobs = (await session.execute(stm)).scalars().all()

    return jobs


@router.get(
    "/jobs",
    status_code=status.HTTP_200_OK,
    response_model=List[JobSchema],
    tags=["Jobs"],
)
async def get_all_jobs(
    session: SessionDep,
    q: Annotated[Optional[str], Query()] = None,
) -> Sequence[JobPosting]:
    """This endpoint will return job postings based on the provided filters."""
    stm = select(JobPosting).options(selectinload(JobPosting.position))

    if q:
        stm = stm.where(JobPosting.description.ilike(f"%{q}%"))

    jobs = (await session.execute(stm)).scalars().all()

    return jobs


@router.get(
    "/jobs/{job_id}",
    status_code=status.HTTP_200_OK,
    response_model=JobSchema,
    tags=["Jobs"],
)
async def get_job_by_id(
    session: SessionDep,
    job_id: str,
) -> JobPosting:
    """Retrieves a specific job posting by its ID."""
    job = await session.get(JobPosting, job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job posting not found.",
        )

    return job


@router.get(
    "/school-jobs/{job_id}",
    status_code=status.HTTP_200_OK,
    response_model=JobSchema,
    tags=["Jobs"],
)
async def get_school_job_by_id(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    job_id: str,
) -> JobPosting:
    """Retrieves a specific job posting by its ID for the authenticated user's school."""
    job = await session.get(JobPosting, job_id)

    if not job or job.school_id != user_in.membership.school_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job posting not found for this school.",
        )

    return job


@router.post(
    "/job-applications",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponse,
    tags=["Jobs"],
)
async def post_job_application(
    session: SessionDep,
    user_in: PlatformAuthenticatedRoute,
    job_id: uuid.UUID,
    application_data: JobApplicationPost,
) -> SuccessResponse:
    """Registers a new job application in the system."""

    job_posting = await session.get(JobPosting, job_id)

    if not job_posting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job posting not found.",
        )

    application = EmploymentApplication(
        school_id=application_data.school_id,
        job_posting_id=application_data.job_id,
        applicant_user_id=application_data.user_id,
        cover_note=application_data.cover_note,
    )

    session.add(application)
    await session.commit()

    return SuccessResponse(id=application.id, message="Job application submitted successfully")


@router.get(
    "/job-applications",
    status_code=status.HTTP_200_OK,
    response_model=List[EmploymentApplicationSchema],
    tags=["Jobs"],
)
async def get_job_applications(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    q: Annotated[Optional[str], Query()] = None,
) -> Sequence[EmploymentApplication]:
    """This endpoint will return job applications based on the provided filters."""
    stm = (
        select(EmploymentApplication)
        .join(EmploymentApplication.job_posting)
        .join(JobPosting.position)
        .join(EmploymentApplication.applicant_user)
        .options(
            selectinload(EmploymentApplication.job_posting).selectinload(JobPosting.position),
            selectinload(EmploymentApplication.applicant_user),
        )
    )

    if q:
        stm = stm.where(Position.title.ilike(f"%{q}%"))

    jobs = (await session.execute(stm)).scalars().all()

    return jobs


@router.post(
    "/job-applications/hire",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponse,
    tags=["Jobs"],
)
async def hire_employee(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    application_form: HireJobApplication,
) -> SuccessResponse:
    """Hire an employee based on a job application."""
    if not user_in.has_permission(PermissionEnum.EMPLOYEES_WRITE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    user_role = RoleEnum.EMPLOYEE  # Default role for new employees
    application = (
        await session.execute(
            select(EmploymentApplication)
            .options(
                selectinload(EmploymentApplication.applicant_user).selectinload(User.memberships),
            )
            .where(
                EmploymentApplication.id == application_form.application_id,
                EmploymentApplication.school_id == user_in.membership.school_id,
            )
        )
    ).scalar_one_or_none()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job application not found for this school.",
        )

    job = (
        await session.execute(
            select(JobPosting)
            .options(selectinload(JobPosting.position))
            .where(
                JobPosting.id == application_form.job_id,
                JobPosting.school_id == user_in.membership.school_id,
            )
        )
    ).scalar_one_or_none()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job posting not found for this school.",
        )

    if application_form.manager_employee_id:
        manager = await session.get(Employee, application_form.manager_employee_id)

        if not manager:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Employee Manager does not exist.",
            )

    # Update application status
    application.status = EmploymentApplicationStatusEnum.ACCEPTED

    if not application.applicant_user.memberships:
        membership = SchoolMembership(
            school_id=user_in.membership.school_id,
            user_id=application.applicant_user_id,
        )
        session.add(membership)
        await session.flush()

    employee = Employee(
        school_id=user_in.membership.school_id,
        user_id=application.applicant_user_id,
        employee_number=application_form.employee_number,
        hire_date=application_form.hire_date,
        employment_status=application_form.employment_status,
        employment_type=application_form.employment_type,
        termination_date=application_form.termination_date,
        manager_employee_id=application_form.manager_employee_id,
        work_email=application_form.work_email,
        work_phone=application_form.work_phone,
    )
    session.add(employee)
    await session.flush()

    employee_position = EmployeePosition(
        school_id=user_in.membership.school_id,
        employee_id=employee.id,
        position_id=job.position.id,
        start_date=application_form.start_date,
        end_date=application_form.end_date,
        is_primary=True,
    )
    session.add(employee_position)

    employment_contract = EmploymentContract(
        school_id=user_in.membership.school_id,
        employee_id=employee.id,
        contract_type=application_form.contract_type,
        start_date=application_form.contract_start_date,
        end_date=application_form.contract_end_date,
        hours_per_week=application_form.hours_per_week,
        status=ContractStatusEnum.ACTIVE,
    )
    session.add(employment_contract)

    if application_form.teacher_profile:
        user_role = RoleEnum.TEACHER
        teacher_profile_data = application_form.teacher_profile
        teacher_profile = TeacherProfile(
            school_id=user_in.membership.school_id,
            employee_id=employee.id,
            specialization=teacher_profile_data.specialization,
            teacher_license_number=teacher_profile_data.teacher_license_number,
            certifications=teacher_profile_data.certification,
            highest_education=teacher_profile_data.highest_education,
            years_of_experience=teacher_profile_data.years_of_experience,
        )
        session.add(teacher_profile)

    role = (await session.execute(select(Role).where(Role.name == user_role))).scalar_one_or_none()

    if not role:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Role not found")

    await ensure_membership_role(
        session,
        membership,
        role,
        user_in.membership.school_id,
    )

    await session.commit()

    return SuccessResponse(id=employee.id, message="Employee hired successfully")
