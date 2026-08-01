#!/usr/bin/python3
"""Public views module for the API"""

import uuid

from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from starlette import status

from project.api.v1.routers.dependencies import (
    AuthenticatedRoute,
    SessionDep,
)
from project.api.v1.routers.registrations.schema import (
    EmployeeRegStep1,
    EmployeeRegStep2,
    EmployeeRegStep3,
    EmployeeRegStep4,
    ParentRegistrationForm,
    ParentRegistrationMe,
    RegistrationResponse,
    RegistrationStep,
    StudentRegistrationMe,
    StudRegStep1,
    StudRegStep2,
    StudRegStep3,
    StudRegStep4,
    StudRegStep5,
)
from project.api.v1.routers.registrations.service import (
    ensure_school_membership,
    link_parent_to_student,
)
from project.core.access_control import get_school_by_id, provision_user_membership
from project.models import User
from project.models.grade import Grade
from project.models.parent import Parent
from project.models.student import Student
from project.utils.enum import MfaStateEnum, RoleEnum

router = APIRouter(prefix="/register", tags=["registration"])


@router.post("/students/step1", response_model=RegistrationStep)
def register_student_step1(session: SessionDep, student_data: StudRegStep1) -> RegistrationStep:
    """Validate student data for each step"""
    return RegistrationStep(message="Student Step 1 Successful")


@router.post("/students/step2", response_model=RegistrationStep)
def register_student_step2(session: SessionDep, student_data: StudRegStep2) -> RegistrationStep:
    """Validate student data for each step"""
    return RegistrationStep(message="Student Step 2 Successful")


@router.post("/students/step3", response_model=RegistrationStep)
def register_student_step3(session: SessionDep, student_data: StudRegStep3) -> RegistrationStep:
    """Validate student data for each step"""
    return RegistrationStep(message="Student Step 3 Successful")


@router.post("/students/step4", response_model=RegistrationStep)
def register_student_step4(session: SessionDep, student_data: StudRegStep4) -> RegistrationStep:
    """Validate student data for each step"""
    return RegistrationStep(message="Student Step 4 Successful")


@router.post("/students/step5", response_model=RegistrationStep)
def register_student_step5(session: SessionDep, student_data: StudRegStep5) -> RegistrationStep:
    """Validate student data for each step"""
    return RegistrationStep(message="Student Step 5 Successful")


@router.post("/parents", status_code=201)
async def register_new_parent(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    parent_data: ParentRegistrationForm,
) -> RegistrationResponse:
    """Registers a new parent in the system."""
    user = await session.execute(select(User).filter(User.email == str(parent_data.email)))
    user = user.scalar_one_or_none()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists",
        )

    user, membership = await provision_user_membership(
        session,
        first_name=parent_data.first_name,
        father_name=parent_data.father_name,
        grand_father_name=parent_data.grand_father_name,
        gender=parent_data.gender,
        date_of_birth=parent_data.date_of_birth,
        school_id=user_in.membership.school_id,
        membership_role_name=RoleEnum.PARENT,
        login_identifier=parent_data.username,
        password=parent_data.password if parent_data.password else None,
        email=str(parent_data.email),
        phone=str(parent_data.phone),
        is_active=False,
        is_verified=False,
        mfa_state=MfaStateEnum.VERIFIED,
    )

    new_parent = Parent(
        school_id=user_in.membership.school_id,
        user_id=user.id,
        relation=parent_data.relation,
        emergency_contact_phone=parent_data.emergency_contact_phone,
    )

    session.add(new_parent)
    await session.commit()

    return RegistrationResponse(id=new_parent.id, message="Parent Registered Successfully")


@router.post("/employees/step1", response_model=RegistrationStep)
def register_employee_step1(
    session: SessionDep,
    employee_data: EmployeeRegStep1,
    user_in: AuthenticatedRoute,
) -> RegistrationStep:
    """Validate employee data for each step"""
    return RegistrationStep(message="Employee Step 1 Successful")


@router.post("/employees/step2", response_model=RegistrationStep)
def register_employee_step2(
    session: SessionDep,
    employee_data: EmployeeRegStep2,
    user_in: AuthenticatedRoute,
) -> RegistrationStep:
    """Validate employee data for each step"""
    return RegistrationStep(message="Employee Step 2 Successful")


@router.post("/employees/step3", response_model=RegistrationStep)
def register_employee_step3(
    session: SessionDep,
    employee_data: EmployeeRegStep3,
    user_in: AuthenticatedRoute,
) -> RegistrationStep:
    """Validate employee data for each step"""
    return RegistrationStep(message="Employee Step 3 Successful")


@router.post("/employees/step4", response_model=RegistrationStep)
def register_employee_step4(
    session: SessionDep,
    employee_data: EmployeeRegStep4,
    user_in: AuthenticatedRoute,
) -> RegistrationStep:
    """Validate employee data for each step"""
    return RegistrationStep(message="Employee Step 4 Successful")


@router.post(
    "/schools/{school_id}/me/parent",
    status_code=201,
    response_model=RegistrationResponse,
)
async def register_me_as_parent(
    school_id: uuid.UUID,
    parent_data: ParentRegistrationMe,
    session: SessionDep,
    current_actor: AuthenticatedRoute,
) -> RegistrationResponse:
    school = await get_school_by_id(session, school_id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")

    await ensure_school_membership(
        session,
        user=current_actor.user,
        school=school,
        role_name=RoleEnum.PARENT,
    )

    new_parent = Parent(
        school_id=school.id,
        user_id=current_actor.user.id,
        relation=parent_data.relation,
        emergency_contact_phone=parent_data.emergency_contact_phone,
    )
    session.add(new_parent)
    await session.commit()

    return RegistrationResponse(id=new_parent.id, message="Registered as Parent successfully")


@router.post(
    "/schools/{school_id}/me/student",
    status_code=201,
    response_model=RegistrationResponse,
)
async def register_me_as_student(
    school_id: uuid.UUID,
    student_data: StudentRegistrationMe,
    session: SessionDep,
    current_actor: AuthenticatedRoute,
) -> RegistrationResponse:
    school = await get_school_by_id(session, school_id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")

    grade = await session.get(Grade, student_data.registered_for_grade_id)
    if not grade or grade.school_id != school.id:
        raise HTTPException(status_code=400, detail="Invalid grade")

    await ensure_school_membership(
        session,
        user=current_actor.user,
        school=school,
        role_name=RoleEnum.STUDENT,
    )

    new_student = Student(
        school_id=school.id,
        user_id=current_actor.user.id,
        city=student_data.city,
        state=student_data.state,
        postal_code=student_data.postal_code,
        nationality=student_data.nationality,
        blood_type=student_data.blood_type,
        student_photo=student_data.student_photo,
        previous_school=student_data.previous_school,
        transportation=student_data.transportation,
        has_medical_condition=student_data.has_medical_condition,
        medical_details=student_data.medical_details,
        has_disability=student_data.has_disability,
        disability_details=student_data.disability_details,
        is_transfer=student_data.is_transfer,
    )
    session.add(new_student)
    await session.flush()

    if student_data.parent_id:
        parent_profile = await session.get(Parent, student_data.parent_id)
        if parent_profile and parent_profile.school_id == school.id:
            await link_parent_to_student(
                session,
                parent_user_id=parent_profile.user_id,
                student_user_id=current_actor.user.id,
            )

    await session.commit()
    return RegistrationResponse(id=new_student.id, message="Registered as Student successfully")
