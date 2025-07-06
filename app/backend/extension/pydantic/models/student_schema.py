from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List
from pydantic import BaseModel, ConfigDict
from datetime import date

from extension.enums.enum import GenderEnum, StudentApplicationStatusEnum
from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .user_schema import UserSchema
    from .student_term_record_schema import StudentTermRecordSchema
    from .student_year_record_schema import StudentYearRecordSchema
    from .subject_yearly_average_schema import SubjectYearlyAverageSchema
    from .assessment_schema import AssessmentSchema


class StudentSchema(BaseModel):
    """
    This model represents a student in the system. It inherits from BaseModel.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    first_name: str
    father_name: str
    date_of_birth: date
    gender: GenderEnum
    address: str
    city: str
    state: str
    postal_code: str
    father_phone: str
    mother_phone: str
    parent_email: str
    grand_father_name: Optional[str] = None
    nationality: Optional[str] = None
    blood_type: Optional[str] = None
    student_photo: Optional[str] = None
    previous_school: Optional[str] = None
    previous_grades: Optional[str] = None
    transportation: Optional[str] = None
    guardian_name: Optional[str] = None
    guardian_phone: Optional[str] = None
    guardian_relation: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    disability_details: Optional[str] = None
    sibling_details: Optional[str] = None
    medical_details: Optional[str] = None
    sibling_in_school: bool = False
    has_medical_condition: bool = False
    has_disability: bool = False
    is_transfer: bool = False
    status: StudentApplicationStatusEnum = StudentApplicationStatusEnum.PENDING
    user_id: Optional[str] = None


class StudentRelationshipSchema(BaseModel):
    """This model represents the relationships of a StudentSchema."""

    user: Optional[UserSchema] = None
    student_term_records: Optional[List[StudentTermRecordSchema]] = None
    student_year_records: Optional[List[StudentYearRecordSchema]] = None
    subject_yearly_averages: Optional[List[SubjectYearlyAverageSchema]] = None
    assessments: Optional[List[AssessmentSchema]] = None