#!/usr/bin/python3
"""Public views module for the API"""

from fastapi import APIRouter

from project.api.v1.routers.dependencies import (
    AuthenticatedRoute,
    SessionDep,
)
from project.api.v1.routers.registrations.schema import (
    EmployeeRegStep1,
    EmployeeRegStep2,
    EmployeeRegStep3,
    EmployeeRegStep4,
    RegistrationStep,
    StudRegStep1,
    StudRegStep2,
    StudRegStep3,
    StudRegStep4,
    StudRegStep5,
)

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
