import random
from typing import Any
from factory import LazyAttribute, SubFactory, post_generation
from extension.enums.enum import AcademicTermTypeEnum
from models.student_year_record import StudentYearRecord
from tests.test_api.factories.student_term_record_factory import (
    StudentTermRecordFactory,
)
from tests.test_api.factories.subject_yearly_average_factory import (
    SubjectYearlyAverageFactory,
)
from .base_factory import BaseFactory
from .grade_factory import GradeFactory
from .year_factory import YearFactory
from models import storage
from models.yearly_subject import YearlySubject


class StudentYearRecordFactory(BaseFactory[StudentYearRecord]):
    class Meta:
        model = StudentYearRecord
        exclude = ("student", "grade", "year", "stream")

    student: Any = SubFactory(
        "tests.test_api.factories.StudentFactory", student_year_records=[]
    )
    year: Any = SubFactory(YearFactory)  # Order Matters
    grade: Any = SubFactory(GradeFactory)
    stream: Any = SubFactory("tests.test_api.factories.StreamFactory")

    @post_generation
    def student_term_records(self, create, extracted, **kwargs):
        if not create:
            return

        num_terms = 2 if self.year.calendar_type == AcademicTermTypeEnum.SEMESTER else 4

        StudentTermRecordFactory.create_batch(
            student_year_record=self,
            student=self.student,
            size=num_terms,
        )

        # Get all YearlySubjects for the given grade
        grade = self.grade
        stream_id = self.stream.id if self.stream else None

        yearly_subjects = (
            storage.session.query(YearlySubject)
            .filter_by(grade_id=grade.id, stream_id=stream_id)
            .all()
        )

        for ys in yearly_subjects:
            SubjectYearlyAverageFactory(
                student=self.student,
                student_year_record=self,
                yearly_subject=ys,
            )

    student_id: Any = LazyAttribute(lambda x: x.student.id)
    grade_id: Any = LazyAttribute(lambda x: x.grade.id)
    stream_id: Any = LazyAttribute(
        lambda x: x.stream.id if x.grade.grade in ["11", "12"] else None
    )
    year_id: Any = LazyAttribute(lambda x: x.year.id)

    final_score: Any = LazyAttribute(lambda _: random.uniform(40.0, 100.0))
    rank: Any = LazyAttribute(lambda _: random.randint(1, 50))
