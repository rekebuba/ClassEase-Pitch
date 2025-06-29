#!/usr/bin/python3
"""Module for Subject class"""

from typing import Dict, List, Optional, TypedDict
from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, mapped_column, scoped_session, relationship, Session
from models.stream import Stream
from models.grade import Grade
from models.base_model import BaseModel
from models.subject_grade_stream_link import SubjectGradeStreamLink
from models.teacher import Teacher


class SubjectDetails(TypedDict):
    grades: List[int]
    stream: Optional[dict[str, List[str]]]


def seed_subjects(session: scoped_session[Session]) -> None:
    """
    Populate the Subject table with default data from grades 1 to 12.

    If the table already has subjects, no data will be added.
    """

    # Check if the table is already populated
    if session.query(Subject).count() > 0:
        return

    subjects: Dict[str, SubjectDetails] = {
        "Arts and Physical Education": {"grades": [1, 2, 3, 4], "stream": None},
        "Environmental Science": {"grades": [1, 2, 3, 4], "stream": None},
        "Integrated Science": {"grades": [5, 6], "stream": None},
        "Social Study": {"grades": [7, 8], "stream": None},
        "Visual Arts and Music": {"grades": [5, 6, 7, 8], "stream": None},
        "Amharic as second language": {"grades": [9, 10], "stream": None},
        "English": {
            "grades": list(range(1, 13)),
            "stream": {"11": ["natural", "social"], "12": ["natural", "social"]},
        },
        "Mathematics": {
            "grades": list(range(1, 13)),
            "stream": {"11": ["natural", "social"], "12": ["natural", "social"]},
        },
        "Mother Tongue": {
            "grades": list(range(1, 13)),
            "stream": {"11": ["natural", "social"], "12": ["natural", "social"]},
        },
        "Amharic": {
            "grades": [1, 2, 3, 4, 5, 6, 7, 8, 11, 12],
            "stream": {"11": ["natural", "social"], "12": ["natural", "social"]},
        },
        "Physical Education": {
            "grades": list(range(5, 13)),
            "stream": {"11": ["natural", "social"], "12": ["natural", "social"]},
        },
        "Civics and Ethical Education": {
            "grades": list(range(5, 13)),
            "stream": {"11": ["natural", "social"], "12": ["natural", "social"]},
        },
        "Biology": {
            "grades": list(range(7, 13)),
            "stream": {"11": ["natural"], "12": ["natural"]},
        },
        "Physics": {
            "grades": list(range(7, 13)),
            "stream": {"11": ["natural"], "12": ["natural"]},
        },
        "Chemistry": {
            "grades": list(range(7, 13)),
            "stream": {"11": ["natural"], "12": ["natural"]},
        },
        "Geography": {
            "grades": [9, 10, 11],
            "stream": {"11": ["social"], "12": ["social"]},
        },
        "History": {
            "grades": [9, 10, 11],
            "stream": {"11": ["social"], "12": ["social"]},
        },
        "Information Technology": {
            "grades": list(range(9, 13)),
            "stream": {"11": ["natural", "social"], "12": ["natural", "social"]},
        },
        "Economics": {
            "grades": [11, 12],
            "stream": {"11": ["social"], "12": ["social"]},
        },
        "General Business": {
            "grades": [11, 12],
            "stream": {"11": ["social"], "12": ["social"]},
        },
        "Technical Drawing": {
            "grades": [11, 12],
            "stream": {"11": ["natural"], "12": ["natural"]},
        },
    }

    for subject_name, details in subjects.items():
        new_subject = Subject(name=subject_name)

        for grade_number in details["grades"]:
            grade_id = session.execute(
                select(Grade.id).where(Grade.grade == grade_number)
            ).scalar_one_or_none()

            if not grade_id:
                raise ValueError(f"Grade {grade_number} not found in the database.")

            streams = (
                details["stream"].get(str(grade_number), None)
                if details["stream"] is not None
                else []
            )

            if streams:
                for stream_name in streams:
                    stream_id = session.execute(
                        select(Stream.id).where(Stream.name == stream_name)
                    ).scalar_one_or_none()

                    if not stream_id:
                        raise ValueError(
                            f"Stream '{stream_name}' not found in the database."
                        )
                    code = generate_code(subject_name, grade_number, stream_name)
                    new_subject.grade_links.append(
                        SubjectGradeStreamLink(
                            subject_id=new_subject.id,
                            grade_id=grade_id,
                            stream_id=stream_id,
                            code=code,
                        )
                    )
            else:
                code = generate_code(subject_name, grade_number, None)
                new_subject.grade_links.append(
                    SubjectGradeStreamLink(
                        subject_id=new_subject.id,
                        grade_id=grade_id,
                        stream_id=None,
                        code=code,
                    )
                )

        session.add(new_subject)

    session.commit()


def generate_code(subject: str, grade: int, stream: Optional[str]) -> str:
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
    # existing_codes = []

    # code = base_code
    # suffix = "-I"

    # while code in existing_codes:
    #     code = f"{base_code}{suffix}"
    #     suffix += "I"

    return base_code


class Subject(BaseModel):
    """
    Subject Model
    """

    __tablename__ = "subjects"
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    teachers: Mapped[List["Teacher"]] = relationship(
        "Teacher",
        back_populates="subjects_to_teach",
        secondary="teacher_subject_links",
        init=False,
        repr=False,
    )
    grade_links: Mapped[List["SubjectGradeStreamLink"]] = relationship(
        "SubjectGradeStreamLink",
        back_populates="subject",
        init=False,
        repr=False,
    )
