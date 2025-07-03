#!/usr/bin/python3
"""Module for Subject class"""

from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel
from models.yearly_subject import YearlySubject

if TYPE_CHECKING:
    from models.teacher import Teacher


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
        default_factory=list,
        repr=False,
    )
    yearly_subjects: Mapped[List["YearlySubject"]] = relationship(
        "YearlySubject",
        back_populates="subject",
        default_factory=list,
        repr=False,
    )
