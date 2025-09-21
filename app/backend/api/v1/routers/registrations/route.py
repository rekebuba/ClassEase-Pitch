#!/usr/bin/python3
"""Public views module for the API"""

from fastapi import APIRouter, HTTPException
from starlette import status

from api.v1.routers.dependencies import SessionDep
from api.v1.routers.registrations.schema import (
    EmployeeRegistrationForm,
    EmployeeRegStep1,
    EmployeeRegStep2,
    EmployeeRegStep3,
    EmployeeRegStep4,
    EmployeeRegStep5,
    RegistrationResponse,
    RegistrationStep,
    StudentRegistrationForm,
    StudRegStep1,
    StudRegStep2,
    StudRegStep3,
    StudRegStep4,
    StudRegStep5,
)
from models.admin import Admin
from models.employee import Employee
from models.grade import Grade
from models.student import Student
from schema.models.admin_schema import AdminSchema

router = APIRouter(prefix="/register", tags=["registration"])


@router.post("/admins", response_model=RegistrationResponse)
def register_new_admin(
    session: SessionDep, admin_data: AdminSchema
) -> RegistrationResponse:
    """Registers a new admin in the system."""

    # Create SQLAlchemy model instance
    new_admin = Admin(
        first_name=admin_data.first_name,
        father_name=admin_data.father_name,
        grand_father_name=admin_data.grand_father_name,
        date_of_birth=admin_data.date_of_birth,
        gender=admin_data.gender,
        email=admin_data.email,
        phone=admin_data.phone,
        address=admin_data.address,
    )

    session.add(new_admin)
    session.commit()

    return RegistrationResponse(
        id=new_admin.id, message="Admin Registered Successfully"
    )


@router.post("/students/step1", response_model=RegistrationStep)
def register_student_step1(
    session: SessionDep, student_data: StudRegStep1
) -> RegistrationStep:
    """Validate student data for each step"""
    return RegistrationStep(message="Student Step 1 Successful")


@router.post("/students/step2", response_model=RegistrationStep)
def register_student_step2(
    session: SessionDep, student_data: StudRegStep2
) -> RegistrationStep:
    """Validate student data for each step"""
    return RegistrationStep(message="Student Step 2 Successful")


@router.post("/students/step3", response_model=RegistrationStep)
def register_student_step3(
    session: SessionDep, student_data: StudRegStep3
) -> RegistrationStep:
    """Validate student data for each step"""
    return RegistrationStep(message="Student Step 3 Successful")


@router.post("/students/step4", response_model=RegistrationStep)
def register_student_step4(
    session: SessionDep, student_data: StudRegStep4
) -> RegistrationStep:
    """Validate student data for each step"""
    return RegistrationStep(message="Student Step 4 Successful")


@router.post("/students/step5", response_model=RegistrationStep)
def register_student_step5(
    session: SessionDep, student_data: StudRegStep5
) -> RegistrationStep:
    """Validate student data for each step"""
    return RegistrationStep(message="Student Step 5 Successful")


@router.post("/students", status_code=201, response_model=RegistrationResponse)
def register_new_student(
    session: SessionDep,
    student_data: StudentRegistrationForm,
) -> RegistrationResponse:
    """Registers a new student in the system."""
    grade = session.get(Grade, student_data.registered_for_grade_id)
    if not grade:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid grade"
        )

    # Convert to dictionary before unpacking
    student_dict = student_data.model_dump(exclude_none=True)

    # Create SQLAlchemy model instance
    new_student = Student(**student_dict)

    session.add(new_student)
    session.commit()

    return RegistrationResponse(
        id=new_student.id, message="Student Registered Successfully"
    )


@router.post("/employees/step1", response_model=RegistrationStep)
def register_employee_step1(
    session: SessionDep, employee_data: EmployeeRegStep1
) -> RegistrationStep:
    """Validate employee data for each step"""
    return RegistrationStep(message="Employee Step 1 Successful")


@router.post("/employees/step2", response_model=RegistrationStep)
def register_employee_step2(
    session: SessionDep, employee_data: EmployeeRegStep2
) -> RegistrationStep:
    """Validate employee data for each step"""
    return RegistrationStep(message="Employee Step 2 Successful")


@router.post("/employees/step3", response_model=RegistrationStep)
def register_employee_step3(
    session: SessionDep, employee_data: EmployeeRegStep3
) -> RegistrationStep:
    """Validate employee data for each step"""
    return RegistrationStep(message="Employee Step 3 Successful")


@router.post("/employees/step4", response_model=RegistrationStep)
def register_employee_step4(
    session: SessionDep, employee_data: EmployeeRegStep4
) -> RegistrationStep:
    """Validate employee data for each step"""
    return RegistrationStep(message="Employee Step 4 Successful")


@router.post("/employees/step5", response_model=RegistrationStep)
def register_employee_step5(
    session: SessionDep, employee_data: EmployeeRegStep5
) -> RegistrationStep:
    """Validate employee data for each step"""
    return RegistrationStep(message="Employee Step 5 Successful")


@router.post("/employees", status_code=201, response_model=RegistrationResponse)
def register_new_employee(
    session: SessionDep,
    employee_data: EmployeeRegistrationForm,
) -> RegistrationResponse:
    """
    Registers a new user (Admin, Student, Employee) in the system.
    """

    # Convert to dictionary before unpacking
    employee_dict = employee_data.model_dump(
        exclude={
            "agree_to_terms",
            "agree_to_background_check",
        },
        exclude_none=True,
    )

    # Create SQLAlchemy model instance
    new_employee = Employee(**employee_dict)

    session.add(new_employee)
    session.commit()

    return RegistrationResponse(
        id=new_employee.id, message="Employee Registered Successfully"
    )
