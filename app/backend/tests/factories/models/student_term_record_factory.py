from typing import Any
from factory import LazyAttribute, SubFactory
from models.student_term_record import StudentTermRecord
from .base_factory import BaseFactory


class StudentTermRecordFactory(BaseFactory[StudentTermRecord]):
    class Meta:
        model = StudentTermRecord
        exclude = ("student", "academic_term", "section", "grade", "stream")

    student: Any = SubFactory("tests.factories.models.StudentFactory", years=[])
    academic_term: Any = SubFactory("tests.factories.models.AcademicTermFactory")
    grade: Any = SubFactory("tests.factories.models.GradeFactory")
    section: Any = SubFactory("tests.factories.models.SectionFactory")
    stream: Any = SubFactory("tests.factories.models.StreamFactory", grade=grade)

    student_id: Any = LazyAttribute(lambda x: x.student.id)
    academic_term_id: Any = LazyAttribute(lambda x: x.academic_term.id)
    grade_id: Any = LazyAttribute(lambda x: x.grade.id)
    section_id: Any = LazyAttribute(lambda x: x.section.id)
    stream_id: Any = LazyAttribute(lambda x: x.stream.id if x.stream else None)

    average: Any = None
    rank: Any = None
