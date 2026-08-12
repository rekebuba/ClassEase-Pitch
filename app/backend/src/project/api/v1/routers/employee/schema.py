import uuid
from datetime import date
from decimal import Decimal
from typing import List, Optional

from pydantic import AwareDatetime

from project.schema.schema import BaseSchema
from project.utils.enum import (
    ContractStatusEnum,
    ContractTypeEnum,
    EmploymentStatusEnum,
    EmploymentTypeEnum,
    HighestEducationEnum,
    PayrollPayFrequencyEnum,
    PayrollPaymentMethodEnum,
)


class EmployeeBasicInfo(BaseSchema):
    id: uuid.UUID
    user_id: Optional[uuid.UUID]
    employee_number: str
    employment_status: EmploymentStatusEnum
    employment_type: EmploymentTypeEnum
    hire_date: date
    termination_date: Optional[date]
    primary_position_id: Optional[uuid.UUID]
    manager_employee_id: Optional[uuid.UUID]
    work_email: Optional[str]
    work_phone: Optional[str]
    created_at: AwareDatetime


class UpdateEmployeeStatusSchema(BaseSchema):
    employee_ids: List[uuid.UUID]
    status: EmploymentStatusEnum


# --- Teacher Profile Schemas ---


class TeacherProfileCreate(BaseSchema):
    employee_id: uuid.UUID
    specialization: Optional[str] = None
    teacher_license_number: Optional[str] = None
    certifications: Optional[str] = None
    highest_education: Optional[HighestEducationEnum] = None
    years_of_experience: Optional[int] = None


class TeacherProfileResponse(TeacherProfileCreate):
    id: uuid.UUID


# --- Lifecycle Schemas ---


class EmployeePositionCreate(BaseSchema):
    employee_id: uuid.UUID
    position_id: uuid.UUID
    start_date: date
    end_date: Optional[date] = None
    is_primary: bool = False


class EmployeePositionUpdate(BaseSchema):
    end_date: Optional[date] = None
    is_primary: Optional[bool] = None


class EmploymentContractCreate(BaseSchema):
    employee_id: uuid.UUID
    contract_type: ContractTypeEnum
    hours_per_week: int
    start_date: date
    end_date: Optional[date] = None
    status: ContractStatusEnum = ContractStatusEnum.DRAFT


class PayrollProfileCreate(BaseSchema):
    employee_id: uuid.UUID
    bank_name: Optional[str] = None
    bank_account: Optional[str] = None
    tin_number: Optional[str] = None
    payment_method: PayrollPaymentMethodEnum
    pay_frequency: PayrollPayFrequencyEnum
    base_salary: Decimal
    currency: str = "ETB"
