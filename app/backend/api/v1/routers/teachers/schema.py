import uuid
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from schema.models.grade_schema import GradeSchema
from schema.models.section_schema import SectionSchema
from schema.models.subject_schema import BasicSubjectSchema
from utils.enum import (
    AcademicTermEnum,
    EmployeeApplicationStatusEnum,
    GenderEnum,
)
from utils.utils import to_camel


class AcademicTermSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )
    name: AcademicTermEnum


class TeacherRecordSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    academic_term: AcademicTermSchema
    grade: GradeSchema
    subject: BasicSubjectSchema
    sections: List[SectionSchema]


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
    gender: GenderEnum
    status: EmployeeApplicationStatusEnum
    teacher_records: List[TeacherRecordSchema]


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
