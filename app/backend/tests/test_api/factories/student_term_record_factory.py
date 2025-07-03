import random
from typing import Any
from factory import (
    LazyAttribute,
    SubFactory,
    SelfAttribute,
    post_generation,
)
from models.student_term_record import StudentTermRecord
from tests.test_api.factories.assessment_factory import AssessmentFactory
from .base_factory import BaseFactory
from models import storage
from models.yearly_subject import YearlySubject


class StudentTermRecordFactory(BaseFactory[StudentTermRecord]):
    class Meta:
        model = StudentTermRecord
        exclude = ("student", "academic_term", "section", "student_year_record")

    student: Any = SubFactory(
        "tests.test_api.factories.StudentFactory", student_year_records=[]
    )
    academic_term: Any = SubFactory("tests.test_api.factories.AcademicTermFactory")
    section: Any = SubFactory(
        "tests.test_api.factories.SectionFactory", student_term_records=[]
    )

    student_year_record: Any = SubFactory(
        "tests.test_api.factories.StudentYearRecordFactory",
        student=SelfAttribute("..student"),
        student_term_records=[],
    )

    @post_generation
    def assessments(self, create, extracted, **kwargs):
        if not create:
            return

        # Get all YearlySubjects for the given grade
        grade = self.student_year_record.grade
        stream_id = (
            self.student_year_record.stream.id
            if self.student_year_record.stream
            else None
        )

        yearly_subjects = (
            storage.session.query(YearlySubject)
            .filter_by(grade_id=grade.id, stream_id=stream_id)
            .all()
        )

        for ys in yearly_subjects:
            AssessmentFactory(
                student=self.student,
                student_term_record=self,
                yearly_subject=ys,
            )

    student_id: Any = LazyAttribute(lambda x: x.student.id)
    academic_term_id: Any = LazyAttribute(lambda x: x.academic_term.id)
    section_id: Any = LazyAttribute(lambda x: x.section.id)
    student_year_record_id: Any = LazyAttribute(lambda x: x.student_year_record.id)

    average: Any = LazyAttribute(lambda _: random.uniform(40.0, 100.0))
    rank: Any = LazyAttribute(lambda _: random.randint(1, 50))
