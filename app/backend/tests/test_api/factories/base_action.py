from enum import Enum
from typing import Dict, List, Optional, Type

from faker import Faker

from extension.enums.enum import (
    AllSubjectsEnum,
    GradeEightSubjectsEnum,
    GradeElevenSubjectsEnum,
    GradeFiveSubjectsEnum,
    GradeFourSubjectsEnum,
    GradeLevelEnum,
    GradeNineSubjectsEnum,
    GradeOneSubjectsEnum,
    GradeSevenSubjectsEnum,
    GradeSixSubjectsEnum,
    GradeTenSubjectsEnum,
    GradeThreeSubjectsEnum,
    GradeTwelveSubjectsEnum,
    GradeTwoSubjectsEnum,
    NaturalStreamSubjectsEnum,
    SectionEnum,
    SocialStreamSubjectsEnum,
    StreamEnum,
)
from models import storage
from models.grade import Grade
from models.section import Section
from models.stream import Stream
from models.subject import Subject
from models.year import Year
from models.yearly_subject import YearlySubject

fake = Faker()


class BaseAction:
    grade_subjects_map: Dict[int, Type[Enum]] = {
        1: GradeOneSubjectsEnum,
        2: GradeTwoSubjectsEnum,
        3: GradeThreeSubjectsEnum,
        4: GradeFourSubjectsEnum,
        5: GradeFiveSubjectsEnum,
        6: GradeSixSubjectsEnum,
        7: GradeSevenSubjectsEnum,
        8: GradeEightSubjectsEnum,
        9: GradeNineSubjectsEnum,
        10: GradeTenSubjectsEnum,
        11: GradeElevenSubjectsEnum,
        12: GradeTwelveSubjectsEnum,
    }

    @staticmethod
    def create_grades() -> None:
        """Populates the grades table with all grades from 1 to 12."""
        for grade_level in range(1, 13):
            if not storage.session.query(Grade).filter_by(grade=grade_level).first():
                grade = Grade(
                    grade=grade_level,
                    level=(
                        GradeLevelEnum.PRIMARY
                        if grade_level < 5
                        else GradeLevelEnum.MIDDLE_SCHOOL
                        if grade_level < 8
                        else GradeLevelEnum.HIGH_SCHOOL
                    ),
                )
                storage.new(grade)
        storage.save()

    @staticmethod
    def create_streams() -> None:
        """Populates the streams table with 'natural' and 'social' streams."""
        for stream_name in StreamEnum:
            if (
                not storage.session.query(Stream)
                .filter_by(name=stream_name.value)
                .first()
            ):
                stream = Stream(name=stream_name.value)
                storage.new(stream)
        storage.save()

    @staticmethod
    def create_section() -> None:
        """Populates the section table with 'A', 'B', and 'C' sections."""
        for section_name in SectionEnum:
            if (
                not storage.session.query(Section)
                .filter_by(section=section_name.value)
                .first()
            ):
                section = Section(section=section_name.value)
                storage.new(section)
        storage.save()

    @staticmethod
    def create_subjects() -> None:
        """Populates the subjects table with all subjects from AllSubjectsEnum."""
        for subject_enum in AllSubjectsEnum:
            if (
                not storage.session.query(Subject)
                .filter_by(name=subject_enum.value)
                .first()
            ):
                subject = Subject(name=subject_enum.value)
                storage.new(subject)
        storage.save()

    @staticmethod
    def _get_grade(grade_level: int) -> Grade:
        """Fetches a grade by its level, raising an error if not found."""
        grade = storage.session.query(Grade).filter_by(grade=grade_level).first()
        if not grade:
            raise ValueError(f"Grade {grade_level} not found in the database")
        return grade

    @staticmethod
    def _get_subject(subject_enum: Enum) -> Subject:
        """Fetches a subject by its enum value, raising an error if not found."""
        subject = (
            storage.session.query(Subject).filter_by(name=subject_enum.value).first()
        )
        if not subject:
            raise ValueError(
                f"Subject '{subject_enum.value}' not found in the database"
            )
        return subject

    @staticmethod
    def _get_stream(stream_enum: StreamEnum) -> Stream:
        """Fetches a stream by its enum value, raising an error if not found."""
        stream = storage.session.query(Stream).filter_by(name=stream_enum.value).first()
        if not stream:
            raise ValueError(f"Stream '{stream_enum.value}' not found in the database")
        return stream

    @staticmethod
    def _create_yearly_subject_if_not_exists(
        year: Year, subject: Subject, grade: Grade, stream: Optional[Stream] = None
    ) -> Optional[YearlySubject]:
        """
        Creates a YearlySubject if it doesn't already exist for the given
        year, subject, grade, and optional stream.
        """
        query = storage.session.query(YearlySubject).filter_by(
            year_id=year.id,
            subject_id=subject.id,
            grade_id=grade.id,
            stream_id=stream.id if stream else None,
        )

        if query.first():
            return None

        return YearlySubject(
            year_id=year.id,
            subject_id=subject.id,
            grade_id=grade.id,
            stream_id=stream.id if stream else None,
        )

    @staticmethod
    def _is_subject_invalid_for_stream(subject_name: str, stream: StreamEnum) -> bool:
        if stream == StreamEnum.SOCIAL:
            return subject_name in NaturalStreamSubjectsEnum._value2member_map_
        if stream == StreamEnum.NATURAL:
            return subject_name in SocialStreamSubjectsEnum._value2member_map_
        return False

    @staticmethod
    def create_necessary_academic_data(year: Year) -> None:
        """
        Orchestrates the creation of all necessary academic records for a new year.
        """
        # 1. Ensure all prerequisite data exists
        BaseAction.create_grades()
        BaseAction.create_streams()
        BaseAction.create_section()
        BaseAction.create_subjects()

        yearly_subjects_to_create: List[YearlySubject] = []

        # 2. Iterate through the grade-to-subject mapping
        for grade_level, subject_enum_class in BaseAction.grade_subjects_map.items():
            grade = BaseAction._get_grade(grade_level)

            for subject_enum in subject_enum_class:
                subject = BaseAction._get_subject(subject_enum)

                # 3. Handle streamed vs. non-streamed grades
                if grade_level in [11, 12]:
                    for stream_enum in StreamEnum:
                        stream = BaseAction._get_stream(stream_enum)

                        # Skip subjects not in the current stream
                        if BaseAction._is_subject_invalid_for_stream(
                            subject.name, StreamEnum(stream.name)
                        ):
                            continue

                        yearly_subject = (
                            BaseAction._create_yearly_subject_if_not_exists(
                                year=year, subject=subject, grade=grade, stream=stream
                            )
                        )
                        if yearly_subject:
                            yearly_subjects_to_create.append(yearly_subject)
                else:
                    yearly_subject = BaseAction._create_yearly_subject_if_not_exists(
                        year=year, subject=subject, grade=grade
                    )
                    if yearly_subject:
                        yearly_subjects_to_create.append(yearly_subject)

        # 4. Bulk save all new YearlySubject objects
        if yearly_subjects_to_create:
            storage.session.bulk_save_objects(yearly_subjects_to_create)
            storage.save()
