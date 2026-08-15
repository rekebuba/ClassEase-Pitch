import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from project.api.v1.routers.school.schema import EmployeeProfile
from project.core.access_control import ensure_user_membership_and_role
from project.models import Employee, User
from project.utils.enum import MfaStateEnum, RoleEnum


class EmployeeService:
    @staticmethod
    async def create_employee_with_membership(
        session: AsyncSession,
        school_id: uuid.UUID,
        employee_data: EmployeeProfile,
    ) -> Employee:
        """
        Handles the creation of an employee and ensures the user has a SchoolMembership
        with the EMPLOYEE role.
        """
        user = (
            await session.execute(
                select(User).where(User.id == employee_data.user_id).options(selectinload(User.memberships))
            )
        ).scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User Not Found",
            )

        if not user.memberships:
            await ensure_user_membership_and_role(
                session=session,
                user_id=user.id,
                school_id=school_id,
                role_enum=RoleEnum.STUDENT,
                mfa_state=MfaStateEnum.VERIFIED,
            )

        if (
            employee_data.manager_employee_id
            and (await session.get(Employee, employee_data.manager_employee_id)) is None
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Manager Employee Not Found",
            )

        employee = Employee(
            school_id=school_id,
            user_id=user.id,
            employee_number=employee_data.employee_number,
            hire_date=employee_data.hire_date,
            employment_status=employee_data.employment_status,
            employment_type=employee_data.employment_type,
            termination_date=employee_data.termination_date,
            manager_employee_id=employee_data.manager_employee_id,
            work_email=employee_data.work_email,
            work_phone=employee_data.work_phone,
        )

        session.add(employee)
        return employee
