import uuid
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from schema.models.subject_schema import BasicSubjectSchema
from utils.enum import (
    EmployeeApplicationStatusEnum,
    GenderEnum,
)
from utils.utils import to_camel


class TeacherSectionDetail(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    section: str
    teacher_subjects: List[BasicSubjectSchema]


class TeacherGradeDetail(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    grade: str
    has_stream: bool
    subjects: List[BasicSubjectSchema]


class TeacherBasicInfo(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    first_name: str
    father_name: str
    grand_father_name: str
    full_name: str
    personal_email: EmailStr = Field(alias="email")
    gender: GenderEnum
    status: EmployeeApplicationStatusEnum
    subject: Optional[BasicSubjectSchema] = Field(alias="mainSubject")
    subjects: List[BasicSubjectSchema] = Field(alias="otherSubjects")
    grades: List[TeacherGradeDetail]


class TeachersQuery(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    q: Optional[str] = None
    year_id: Optional[uuid.UUID] = None
    academic_term_id: Optional[uuid.UUID] = None


class SectionIDs(BaseModel):
    id: uuid.UUID


class AssignGrade(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    stream_id: Optional[uuid.UUID]
    sections: List[SectionIDs] = Field(min_length=1)


class AssignTeacher(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    year_id: uuid.UUID
    teacher_id: uuid.UUID
    subject_id: uuid.UUID
    grade: AssignGrade
