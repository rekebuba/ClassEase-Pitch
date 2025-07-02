import random
from typing import Any
from factory import LazyAttribute, SubFactory, RelatedFactoryList, SelfAttribute
from models.student_year_record import StudentYearRecord
from .base_factory import BaseFactory
from .grade_factory import GradeFactory
from .year_factory import YearFactory


class StudentYearRecordFactory(BaseFactory[StudentYearRecord]):
    class Meta:
        model = StudentYearRecord
        exclude = ("student", "grade", "year")

    student: Any = SubFactory(
        "tests.test_api.factories.StudentFactory", student_year_records=[]
    )
    grade: Any = SubFactory(GradeFactory)
    year: Any = SubFactory(YearFactory)

    student_semester_records: Any = RelatedFactoryList(
        "tests.test_api.factories.StudentSemesterRecordFactory",
        factory_related_name="student_year_record",
        student=SelfAttribute("..student"),
        size=2,
    )

    student_id: Any = LazyAttribute(lambda x: x.student.id)
    grade_id: Any = LazyAttribute(lambda x: x.grade.id)
    year_id: Any = LazyAttribute(lambda x: x.year.id)

    final_score: Any = LazyAttribute(lambda _: random.uniform(40.0, 100.0))
    rank: Any = LazyAttribute(lambda _: random.randint(1, 50))
