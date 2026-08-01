from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List, Optional

from project.schema.schema import BaseSchema

if TYPE_CHECKING:
    from project.schema.models.academic_term_schema import AcademicTermSchema
    from project.schema.models.grade_schema import GradeSchema
    from project.schema.models.mark_list_schema import MarkListSchema
    from project.schema.models.section_schema import SectionSchema
    from project.schema.models.stream_schema import StreamSchema
    from project.schema.models.student_schema import StudentSchema


class StudentTermRecordSchema(BaseSchema):
    """
    This model represents the average result of a student
    for a particular term and year.
    """

    id: uuid.UUID | None = None
    student_id: uuid.UUID
    academic_term_id: uuid.UUID
    grade_id: uuid.UUID
    section_id: uuid.UUID
    stream_id: Optional[uuid.UUID] = None

    average: Optional[float] = None
    rank: Optional[int] = None


class StudentTermRecordRelatedSchema(BaseSchema):
    """This model represents the relationships of a StudentTermRecordSchema."""

    student: Optional[StudentSchema] = None
    academic_term: Optional[AcademicTermSchema] = None
    grade: Optional[GradeSchema] = None
    section: Optional[SectionSchema] = None
    stream: Optional[StreamSchema] = None
    mark_lists: Optional[List[MarkListSchema]]


class StudentTermRecordWithRelatedSchema(StudentTermRecordSchema, StudentTermRecordRelatedSchema):
    """
    This model combines the StudentTermRecordSchema with its relationships.
    It is used to provide a complete view of a student's term record
    along with related entities.
    """

    pass
