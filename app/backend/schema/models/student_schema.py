from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from utils.enum import BloodTypeEnum, GenderEnum, StudentApplicationStatusEnum
from utils.utils import to_camel

if TYPE_CHECKING:
    from .academic_term_schema import AcademicTermSchema
    from .assessment_schema import AssessmentSchema
    from .grade_schema import GradeSchema
    from .mark_list_schema import MarkListSchema
    from .section_schema import SectionSchema
    from .student_term_record_schema import StudentTermRecordSchema
    from .student_year_record_schema import StudentYearRecordSchema
    from .subject_schema import SubjectSchema
    from .subject_yearly_average_schema import SubjectYearlyAverageSchema
    from .user_schema import UserSchema
    from .year_schema import YearSchema


class StudentSchema(BaseModel):
    """
    This model represents a student in the system. It inherits from BaseModel.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
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
    blood_type: BloodTypeEnum = BloodTypeEnum.UNKNOWN
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
    user_id: Optional[uuid.UUID] = None

    @classmethod
    def default_fields(cls) -> set[str]:
        """
        Returns a list of default fields to be used when no specific fields are requested.
        This can be overridden in subclasses if needed.
        """
        return {"id", "first_name", "father_name", "date_of_birth"}


class StudentRelatedSchema(BaseModel):
    """This model represents the relationships of a StudentSchema."""

    starting_grade: Optional[GradeSchema]
    user: Optional[UserSchema]
    term_records: List[StudentTermRecordSchema]
    student_year_records: List[StudentYearRecordSchema]
    subject_yearly_averages: List[SubjectYearlyAverageSchema]
    assessments: List[AssessmentSchema]

    years: List[YearSchema] = Field(
        description="List of years the student is associated with.",
    )
    academic_terms: List[AcademicTermSchema] = Field(
        description="List of academic terms the student is associated with.",
    )
    grades: List[GradeSchema] = Field(
        description="List of grades the student is associated with.",
    )
    subjects: List[SubjectSchema] = Field(
        description="List of subjects the student is associated with.",
    )
    sections: List[SectionSchema] = Field(
        description="List of sections the student is associated with.",
    )
    mark_lists: List[MarkListSchema] = Field(
        description="List of mark lists associated with the student.",
    )


class StudentWithRelatedSchema(StudentSchema, StudentRelatedSchema):
    pass
