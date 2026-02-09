#!/usr/bin/python3
"""Public views module for the API"""

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import NameEmail
from starlette import status

from project.api.v1.routers.auth.service import send_verification_email
from project.api.v1.routers.dependencies import SessionDep, admin_route
from project.api.v1.routers.registrations.schema import (
    AdminRegistration,
    EmployeeRegistrationForm,
    EmployeeRegStep1,
    EmployeeRegStep2,
    EmployeeRegStep3,
    EmployeeRegStep4,
    ParentRegistrationForm,
    RegistrationResponse,
    RegistrationStep,
    StudentRegistrationForm,
    StudRegStep1,
    StudRegStep2,
    StudRegStep3,
    StudRegStep4,
    StudRegStep5,
)
from project.core.security import get_password_hash
from project.models import User
from project.models.admin import Admin
from project.models.employee import Employee
from project.models.grade import Grade
from project.models.parent import Parent
from project.models.parent_student_link import ParentStudentLink
from project.models.student import Student
from project.utils.enum import RoleEnum

router = APIRouter(prefix="/register", tags=["registration"])


@router.post("/admins", status_code=201, response_model=RegistrationResponse)
def register_new_admin(
    session: SessionDep,
    admin_data: AdminRegistration,
    user_in: admin_route,
    background_tasks: BackgroundTasks,
) -> RegistrationResponse:
    """Registers a new admin in the system."""
    hash_password = get_password_hash(admin_data.password)

    user = User(
        username=admin_data.username,
        password=hash_password,
        role=RoleEnum.ADMIN,
        email=admin_data.email,
        phone=admin_data.phone,
        is_active=False,
    )

    session.add(user)
    session.flush()

    # Create SQLAlchemy model instance
    new_admin = Admin(
        user_id=user.id,
        first_name=admin_data.first_name,
        father_name=admin_data.father_name,
        grand_father_name=admin_data.grand_father_name,
        date_of_birth=admin_data.date_of_birth,
        gender=admin_data.gender,
    )

    session.add(new_admin)
    session.commit()

    background_tasks.add_task(
        send_verification_email, NameEmail(name=new_admin.first_name, email=user.email)
    )

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


@router.post("/parents", status_code=201)
def register_new_parent(
    session: SessionDep,
    user_id: admin_route,
    parent_data: ParentRegistrationForm,
) -> RegistrationResponse:
    """Registers a new parent in the system."""
    # Create SQLAlchemy model instance
    new_parent = Parent(
        first_name=parent_data.first_name,
        last_name=parent_data.last_name,
        gender=parent_data.gender,
        email=parent_data.email,
        phone=parent_data.phone,
        relation=parent_data.relation,
        emergency_contact_phone=parent_data.emergency_contact_phone,
    )

    session.add(new_parent)
    session.commit()

    return RegistrationResponse(
        id=new_parent.id, message="Parent Registered Successfully"
    )


@router.post("/students", status_code=201, response_model=RegistrationResponse)
def register_new_student(
    session: SessionDep,
    student_data: StudentRegistrationForm,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid grade or parent ID"}
    },
) -> RegistrationResponse:
    """Registers a new student in the system."""
    grade = session.get(Grade, student_data.registered_for_grade_id)
    if not grade:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid grade"
        )
    parent = session.get(Parent, student_data.parent_id)
    if not parent:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid parent"
        )

    # Create SQLAlchemy model instance
    new_student = Student(
        first_name=student_data.first_name,
        father_name=student_data.father_name,
        grand_father_name=student_data.grand_father_name,
        date_of_birth=student_data.date_of_birth,
        gender=student_data.gender,
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
        registered_for_grade_id=grade.id,
    )

    session.add(new_student)
    session.flush()

    student_parent_link = ParentStudentLink(
        parent_id=parent.id, student_id=new_student.id
    )

    session.add(student_parent_link)
    session.commit()

    return RegistrationResponse(
        id=new_student.id, message="Student Registered Successfully"
    )


@router.post("/employees/step1", response_model=RegistrationStep)
def register_employee_step1(
    session: SessionDep,
    employee_data: EmployeeRegStep1,
    user_in: admin_route,
) -> RegistrationStep:
    """Validate employee data for each step"""
    return RegistrationStep(message="Employee Step 1 Successful")


@router.post("/employees/step2", response_model=RegistrationStep)
def register_employee_step2(
    session: SessionDep,
    employee_data: EmployeeRegStep2,
    user_in: admin_route,
) -> RegistrationStep:
    """Validate employee data for each step"""
    return RegistrationStep(message="Employee Step 2 Successful")


@router.post("/employees/step3", response_model=RegistrationStep)
def register_employee_step3(
    session: SessionDep,
    employee_data: EmployeeRegStep3,
    user_in: admin_route,
) -> RegistrationStep:
    """Validate employee data for each step"""
    return RegistrationStep(message="Employee Step 3 Successful")


@router.post("/employees/step4", response_model=RegistrationStep)
def register_employee_step4(
    session: SessionDep,
    employee_data: EmployeeRegStep4,
    user_in: admin_route,
) -> RegistrationStep:
    """Validate employee data for each step"""
    return RegistrationStep(message="Employee Step 4 Successful")


@router.post("/employees", status_code=201, response_model=RegistrationResponse)
def register_new_employee(
    session: SessionDep,
    employee_data: EmployeeRegistrationForm,
    user_in: admin_route,
) -> RegistrationResponse:
    """
    Registers a new user (Admin, Student, Employee) in the system.
    """

    # Create SQLAlchemy model instance
    new_employee = Employee(
        first_name=employee_data.first_name,
        father_name=employee_data.father_name,
        grand_father_name=employee_data.grand_father_name,
        date_of_birth=employee_data.date_of_birth,
        gender=employee_data.gender,
        nationality=employee_data.nationality,
        social_security_number=employee_data.social_security_number,
        city=employee_data.city,
        state=employee_data.state,
        country=employee_data.country,
        emergency_contact_name=employee_data.emergency_contact_name,
        emergency_contact_relation=employee_data.emergency_contact_relation,
        emergency_contact_phone=employee_data.emergency_contact_phone,
        highest_education=employee_data.highest_education,
        university=employee_data.university,
        graduation_year=employee_data.graduation_year,
        gpa=employee_data.gpa,
        position=employee_data.position,
        years_of_experience=employee_data.years_of_experience,
    )

    session.add(new_employee)
    session.commit()

    return RegistrationResponse(
        id=new_employee.id, message="Employee Registered Successfully"
    )
