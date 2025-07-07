#!/usr/bin/python3
import random
from typing import Any, List
from factory import SubFactory, LazyAttribute, post_generation
from sqlalchemy import and_, exists, select
from extension.enums.enum import MarkListTypeEnum
from models.assessment import Assessment
from models.mark_list import MarkList
from models.student_term_record import StudentTermRecord
from models.teacher_record import TeachersRecord
from models.teacher_record_section_link import TeacherRecordSectionLink
from models.teacher_yearly_subject_link import TeacherYearlySubjectLink
from models.yearly_subject import YearlySubject
from .mark_list_factory import MarkListFactory
from .section_factory import SectionFactory
from .base_factory import BaseFactory
from models import storage


class TeacherRecordFactory(BaseFactory[TeachersRecord]):
    class Meta:
        model = TeachersRecord
        exclude = ("teacher", "academic_term", "section")

    academic_term: Any = SubFactory("tests.factories.models.AcademicTermFactory")
    teacher: Any = SubFactory(
        "tests.factories.models.TeacherFactory", teacher_records=[]
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

        subq = select(TeacherYearlySubjectLink.yearly_subject_id).where(
            TeacherYearlySubjectLink.yearly_subject_id == YearlySubject.id,
        )

        assigned_yearly_subject = (
            storage.session.query(YearlySubject)
            .join(YearlySubject.grade)
            .join(YearlySubject.subject)
            .where(
                YearlySubject.grade_id.in_(
                    [grade.id for grade in self.teacher.grade_to_teach]
                ),
                YearlySubject.subject_id.in_(
                    [subject.id for subject in self.teacher.subjects_to_teach]
                ),
                ~exists(subq),  # this ensures there's no existing link
            )
        ).all()

        if not assigned_yearly_subject:
            return

        self.yearly_subjects_link.extend(
            random.sample(
                assigned_yearly_subject,
                k=random.randint(1, len(assigned_yearly_subject) or 1),
            )
        )
        storage.session.commit()

        my_students = (
            storage.session.query(
                Assessment.yearly_subject_id,
                StudentTermRecord.student_id,
                StudentTermRecord.academic_term_id,
            )
            .join(
                StudentTermRecord,
                Assessment.student_term_record_id == StudentTermRecord.id,
            )
            .join(
                TeachersRecord,
                StudentTermRecord.academic_term_id == TeachersRecord.academic_term_id,
            )
            .join(
                TeacherRecordSectionLink,
                and_(
                    TeachersRecord.id == TeacherRecordSectionLink.teacher_record_id,
                    StudentTermRecord.section_id == TeacherRecordSectionLink.section_id,
                ),
            )
            .join(
                TeacherYearlySubjectLink,
                and_(
                    TeachersRecord.id == TeacherYearlySubjectLink.teacher_record_id,
                    Assessment.yearly_subject_id
                    == TeacherYearlySubjectLink.yearly_subject_id,
                ),
            )
            .distinct()
            .filter(
                TeachersRecord.teacher_id == self.teacher.id,
            )
        ).all()

        percentages = [10, 5, 5, 30, 50]
        mark_list: List[MarkList] = []
        for student in my_students:
            for i, type in enumerate(MarkListTypeEnum):
                mark_list.append(
                    MarkList(
                        student_id=student.student_id,
                        academic_term_id=student.academic_term_id,
                        yearly_subject_id=student.yearly_subject_id,
                        type=type,
                        percentage=percentages[i % len(percentages)],
                    )
                )

        if mark_list:
            storage.session.bulk_save_objects(mark_list)
            storage.save()

    teacher_id: Any = LazyAttribute(lambda x: x.teacher.id)
    academic_term_id: Any = LazyAttribute(lambda x: x.academic_term.id)
