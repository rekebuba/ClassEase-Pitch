from typing import List

from project.schema.schema import BaseSchema
from project.utils.enum import (
    GradeEnum,
    GradeLevelEnum,
)


class SubjectTemplate(BaseSchema):
    name: str
    code: str


class SectionTemplate(BaseSchema):
    section: str


class StreamTemplate(BaseSchema):
    name: str
    subjects: List[SubjectTemplate]


class GradeTemplate(BaseSchema):
    grade: GradeEnum
    level: GradeLevelEnum
    has_stream: bool
    subjects: List[SubjectTemplate]
    streams: List[StreamTemplate]


class BluePrintTemplate(BaseSchema):
    subjects: List[SubjectTemplate]
    sections: List[SectionTemplate]
    grades: List[GradeTemplate]
