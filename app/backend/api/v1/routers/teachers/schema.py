import uuid
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from schema.models.grade_schema import GradeSchema
from schema.models.section_schema import SectionSchema
from schema.models.subject_schema import BasicSubjectSchema
from utils.enum import (
    EmployeeApplicationStatusEnum,
    GenderEnum,
)
from utils.utils import to_camel


class TeacherRecordSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    grade: GradeSchema
    subject: BasicSubjectSchema
    section: SectionSchema


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
    subject: BasicSubjectSchema
    subjects: List[BasicSubjectSchema]
    grades: List[GradeSchema | None]


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
