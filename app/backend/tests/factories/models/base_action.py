from enum import Enum
import random
from typing import Dict, List, Optional, Type

from faker import Faker
from sqlalchemy import select

from extension.enums.enum import (
    AcademicTermEnum,
    AcademicTermTypeEnum,
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
from models.academic_term import AcademicTerm
from models.grade import Grade
from models.section import Section
from models.stream import Stream
from models.subject import Subject
from models.year import Year
from models.yearly_subject import YearlySubject
from models.grade_section_link import GradeSectionLink

fake = Faker()


class BaseAction:
    grade_subjects_map: Dict[str, Type[Enum]] = {
        "1": GradeOneSubjectsEnum,
        "2": GradeTwoSubjectsEnum,
        "3": GradeThreeSubjectsEnum,
        "4": GradeFourSubjectsEnum,
        "5": GradeFiveSubjectsEnum,
        "6": GradeSixSubjectsEnum,
        "7": GradeSevenSubjectsEnum,
        "8": GradeEightSubjectsEnum,
        "9": GradeNineSubjectsEnum,
        "10": GradeTenSubjectsEnum,
        "11": GradeElevenSubjectsEnum,
        "12": GradeTwelveSubjectsEnum,
    }

    @staticmethod
    def create_academic_term(year: Year) -> None:
        """
        Creates academic terms for the given year based on its type.
        """
        # Check if academic terms already exist for the year
        existing_terms = (
            storage.session.query(AcademicTerm).filter_by(year_id=year.id).all()
        )
        if existing_terms:
            return

        academic_term = [
            AcademicTerm(
                year_id=year.id,
                name=term,
                start_date=fake.past_date(),
                end_date=fake.future_date(),
                registration_start=fake.past_date(),
                registration_end=fake.future_date(),
            )
            for term in list(AcademicTermEnum)[
                : 4 if year.calendar_type == AcademicTermTypeEnum.QUARTER else 2
            ]
        ]

        storage.session.bulk_save_objects(academic_term)
        storage.save()

    @staticmethod
    def create_grades(year: Year, sections: List[Section]) -> None:
        """Populates the grades table with all grades from 1 to 12."""
        if storage.session.query(Grade).count() > 0:
            return

        social_stream = (
            storage.session.query(Stream)
            .filter_by(name=StreamEnum.SOCIAL.value)
            .first()
        )
        natural_stream = (
            storage.session.query(Stream)
            .filter_by(name=StreamEnum.NATURAL.value)
            .first()
        )

        grade_link = []
        for grade_level in range(1, 13):
            grade = Grade(
                year_id=year.id,
                grade=str(grade_level),
                level=(
                    GradeLevelEnum.PRIMARY
                    if grade_level < 5
                    else GradeLevelEnum.MIDDLE_SCHOOL
                    if grade_level < 8
                    else GradeLevelEnum.HIGH_SCHOOL
                ),
                has_stream=grade_level in [11, 12],
            )

            if grade_level > 10:
                if not social_stream or not natural_stream:
                    continue  # Ensure streams exist before assigning

                # Assign streams to grades 11 and 12
                grade.streams = [social_stream, natural_stream]

            storage.new(grade)
            storage.session.flush()  # Ensure the new Grade is saved

            grade_link.extend(
                [
                    GradeSectionLink(
                        section_id=section.id,
                        grade_id=grade.id,
                    )
                    for section in sections[: random.randint(1, len(sections))]
                ]
            )

        storage.session.bulk_save_objects(grade_link)
        storage.save()

    @staticmethod
    def create_streams(year: Year) -> None:
        """Populates the streams table with 'natural' and 'social' streams."""
        if storage.session.query(Stream).count() == len(StreamEnum):
            return

        for stream_name in StreamEnum:
            if (
                not storage.session.query(Stream)
                .filter_by(name=stream_name.value)
                .first()
            ):
                stream = Stream(year_id=year.id, name=stream_name.value)
                storage.new(stream)
        storage.save()

    @staticmethod
    def create_section(year: Year) -> None:
        """Populates the section table with 'A', 'B', and 'C' sections."""
        if storage.session.query(Section).count() > 0:
            return

        for section_name in SectionEnum:
            section = Section(year_id=year.id, section=section_name.value)
            storage.new(section)

        storage.save()

    @staticmethod
    def create_subjects(year: Year) -> None:
        """Populates the subjects table with all subjects from AllSubjectsEnum."""
        if storage.session.query(Subject).count() == len(AllSubjectsEnum):
            return

        for subject_enum in AllSubjectsEnum:
            if (
                not storage.session.query(Subject)
                .filter_by(name=subject_enum.value)
                .first()
            ):
                # Split the subject name into words
                words = subject_enum.value.split()

                # Determine the length of the prefix for each word (2 letters if multiple words, 3 otherwise)
                prefix_length = 3

                # Generate the base code by taking the first 'prefix_length' characters of each word and converting them to uppercase
                code = "".join(
                    [
                        word[:prefix_length].upper()
                        for word in words
                        if word.isalpha() and word != "and"
                    ]
                )
                subject = Subject(year_id=year.id, name=subject_enum.value, code=code)
                storage.new(subject)
        storage.save()

    @staticmethod
    def _get_grade(grade_level: str) -> Grade:
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
        year: Year,
        subject: Subject,
        grade: Grade,
        stream: Optional[Stream] = None,
    ) -> None:
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
        # Generate a unique subject code
        subject_code = BaseAction._generate_subject_code(
            subject=subject.name,
            grade=grade.grade,
            year_id=year.id,
            stream=stream.name if stream else None,
        )

        new_yearly_subject = YearlySubject(
            year_id=year.id,
            subject_id=subject.id,
            grade_id=grade.id,
            stream_id=stream.id if stream else None,
            subject_code=subject_code,
        )

        storage.new(new_yearly_subject)
        storage.session.commit()

    @staticmethod
    def _is_subject_invalid_for_stream(subject_name: str, stream: StreamEnum) -> bool:
        if stream == StreamEnum.SOCIAL:
            return subject_name in NaturalStreamSubjectsEnum._value2member_map_
        if stream == StreamEnum.NATURAL:
            return subject_name in SocialStreamSubjectsEnum._value2member_map_
        return False

    @staticmethod
    def _generate_subject_code(
        subject: str,
        grade: str,
        year_id: str,
        stream: Optional[str],
    ) -> str:
        """
        Generate a unique code for the subject.

        Args:
            prev_data (list): Previously generated Subject objects to check for duplicates.
            subject (str): Subject name.
            grade (int): Grade level.
        """

        # Split the subject name into words
        words = subject.split()

        # Determine the length of the prefix for each word (2 letters if multiple words, 3 otherwise)
        prefix_length = 3

        # Generate the base code by taking the first 'prefix_length' characters of each word and converting them to uppercase
        base_code = "".join(
            [
                word[:prefix_length].upper()
                for word in words
                if word.isalpha() and word != "and"
            ]
        )

        # Append the grade number to the base code
        base_code += str(grade)

        # Append the stream to the base code
        if stream:
            base_code += f"-{stream[0].upper()}"

        # Check for existing codes in the database
        existing_codes = storage.session.scalars(
            select(YearlySubject.subject_code).where(YearlySubject.year_id == year_id)
        ).all()

        code = base_code
        suffix = "-I"

        while code in existing_codes:
            code = f"{base_code}{suffix}"
            suffix += "I"

        return base_code

    @staticmethod
    def create_necessary_academic_data(year: Year) -> None:
        """
        Orchestrates the creation of all necessary academic records for a new year.
        """
        # 1. Ensure all prerequisite data exists
        BaseAction.create_academic_term(year)
        BaseAction.create_streams(year)  # Order Maters
        BaseAction.create_section(year)
        BaseAction.create_subjects(year)

        sections = storage.session.scalars(select(Section)).all()
        BaseAction.create_grades(year, list(sections))

        # 2. Iterate through the grade-to-subject mapping
        for grade_level, subject_enum_class in BaseAction.grade_subjects_map.items():
            grade = BaseAction._get_grade(grade_level)

            for subject_enum in subject_enum_class:
                subject = BaseAction._get_subject(subject_enum)

                # 3. Handle streamed vs. non-streamed grades
                if grade_level in ["11", "12"]:
                    for stream_enum in StreamEnum:
                        stream = BaseAction._get_stream(stream_enum)

                        # Skip subjects not in the current stream
                        if BaseAction._is_subject_invalid_for_stream(
                            subject.name, StreamEnum(stream.name)
                        ):
                            continue
                        BaseAction._create_yearly_subject_if_not_exists(
                            year=year,
                            subject=subject,
                            grade=grade,
                            stream=stream,
                        )
                else:
                    BaseAction._create_yearly_subject_if_not_exists(
                        year=year,
                        subject=subject,
                        grade=grade,
                    )

        storage.save()
