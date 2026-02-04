from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

from project.utils.enum import BloodTypeEnum, GenderEnum, StudentApplicationStatusEnum
from project.utils.utils import to_camel

if TYPE_CHECKING:
    from project.schema.models.academic_term_schema import AcademicTermSchema
    from project.schema.models.assessment_schema import AssessmentSchema
    from project.schema.models.grade_schema import GradeSchema
    from project.schema.models.mark_list_schema import MarkListSchema
    from project.schema.models.section_schema import SectionSchema
    from project.schema.models.student_term_record_schema import StudentTermRecordSchema
    from project.schema.models.student_year_record_schema import StudentYearRecordSchema
    from project.schema.models.subject_schema import SubjectSchema
    from project.schema.models.subject_yearly_average_schema import SubjectYearlyAverageSchema
    from project.schema.models.user_schema import UserSchema
    from project.schema.models.year_schema import YearSchema


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
    father_phone: PhoneNumber
    mother_phone: PhoneNumber
    parent_email: EmailStr
    grand_father_name: Optional[str]
    nationality: Optional[str]
    blood_type: BloodTypeEnum = BloodTypeEnum.UNKNOWN
    student_photo: Optional[str]
    previous_school: Optional[str]
    previous_grades: Optional[str]
    transportation: Optional[str]
    guardian_name: Optional[str]
    guardian_phone: Optional[PhoneNumber]
    guardian_relation: Optional[str]
    emergency_contact_name: Optional[str]
    emergency_contact_phone: Optional[str]
    disability_details: Optional[str]
    sibling_details: Optional[str]
    medical_details: Optional[str]
    sibling_in_school: bool
    has_medical_condition: bool
    has_disability: bool
    is_transfer: bool
    status: StudentApplicationStatusEnum = StudentApplicationStatusEnum.PENDING
    user_id: Optional[uuid.UUID]

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
