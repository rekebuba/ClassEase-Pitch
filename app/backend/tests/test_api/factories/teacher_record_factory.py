#!/usr/bin/python3
import random
from typing import Any, List
from factory import SubFactory, LazyAttribute, post_generation
from models.teacher_record import TeachersRecord
from models.yearly_subject import YearlySubject
from tests.test_api.factories.section_factory import SectionFactory
from .base_factory import BaseFactory
from models import storage


class TeacherRecordFactory(BaseFactory[TeachersRecord]):
    class Meta:
        model = TeachersRecord
        exclude = ("teacher", "academic_term", "section")

    academic_term: Any = SubFactory("tests.test_api.factories.AcademicTermFactory")
    teacher: Any = SubFactory(
        "tests.test_api.factories.TeacherFactory", teacher_records=[]
    )

    sections_link: Any = LazyAttribute(
        lambda _: SectionFactory.create_batch(
            size=random.randint(1, 3), student_term_records=[]
        )
    )
    yearly_subjects_link: List[YearlySubject] = []

    @post_generation
    def yearly_subjects(self, create, extracted, **kwargs):
        if not create:
            return

        # Assign yearly subjects to the teacher record
        if extracted:
            self.yearly_subjects_link.extend(extracted)
        else:
            assigned_yearly_subject = (
                storage.session.query(YearlySubject)
                .join(YearlySubject.grade)
                .join(YearlySubject.subject)
                .where(
                    YearlySubject.grade_id.in_(
                        [grade.id for grade in self.teacher.grade_level]
                    ),
                    YearlySubject.subject_id.in_(
                        [subject.id for subject in self.teacher.subjects_to_teach]
                    ),
                )
            ).all()

            self.yearly_subjects_link.extend(
                random.sample(
                    assigned_yearly_subject,
                    k=random.randint(1, len(assigned_yearly_subject) or 1),
                )
            )
            storage.session.commit()
            
            

    teacher_id: Any = LazyAttribute(lambda x: x.teacher.id)
    academic_term_id: Any = LazyAttribute(lambda x: x.academic_term.id)
