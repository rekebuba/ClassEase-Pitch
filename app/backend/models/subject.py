#!/usr/bin/python3
""" Module for Subject class """

import uuid
from sqlalchemy import CheckConstraint, Integer, String, ForeignKey
from models.stream import Stream
from models.grade import Grade
from models.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column


def seed_subjects(session):
    """
    Populate the Subject table with default data (from grade 1 to 12).

    This function checks if the Subject table is empty. If it is, it populates
    the table with subjects grade 1 to 12. If the table already contains data,
    the function does nothing.

    Args:
        session (Session): SQLAlchemy session object used to interact with the database.

    """
    subject_per_grade = {
        "1-4": [
            "Arts and Physical Education",
            "Mother Tongue",
            "Mathematics",
            "Amharic",
            "English",
            "Environmental Science",
        ],
        "5-6": [
            "Civics and Ethical Education",
            "Mother Tongue",
            "Mathematics",
            "Amharic",
            "English",
            "Visual Arts and Music",
            "Physical Education",
            "Integrated Science",
        ],
        "7-8": [
            "Civics and Ethical Education",
            "Mother Tongue",
            "Mathematics",
            "Amharic",
            "English",
            "Visual Arts and Music",
            "Physical Education",
            "Biology",
            "Chemistry",
            "Physics",
            "Social Study",
        ],
        "9-10": [
            "Civics and Ethical Education",
            "Mother Tongue",
            "Mathematics",
            "Amharic as second language",
            "English",
            "Physical Education",
            "Biology",
            "Chemistry",
            "Physics",
            "Geography",
            "History",
            "Information Technology",
        ],
        "11-12(Natural)": [
            "Civics and Ethical Education",
            "Mother Tongue",
            "Mathematics",
            "Amharic",
            "English",
            "Physical Education",
            "Biology",
            "Chemistry",
            "Physics",
            "Information Technology",
            "Technical Drawing",
        ],
        "11-12(Social)": [
            "Civics and Ethical Education",
            "Mother Tongue",
            "Mathematics",
            "Amharic",
            "English",
            "Physical Education",
            "Geography",
            "History",
            "Information Technology",
            "Economics",
            "General Business"
        ]
    }
    # Check if the table is already populated
    if session.query(Subject).count() > 0:
        return

    bulk_insert = []

    # Preload stream IDs once
    streams = {s.name: s.id for s in session.query(Stream).all()}
    for grade in range(1, 13):
        grade_id = session.query(Grade.id).filter_by(name=grade).scalar()
        if 1 <= grade <= 4:
            subjects = subject_per_grade["1-4"]
        elif 5 <= grade <= 6:
            subjects = subject_per_grade["5-6"]
        elif 7 <= grade <= 8:
            subjects = subject_per_grade["7-8"]
        elif 9 <= grade <= 10:
            subjects = subject_per_grade["9-10"]
        elif 11 <= grade <= 12:
            for stream, subject_list in [("natural", "11-12(Natural)"), ("social", "11-12(Social)")]:
                for subject in subject_per_grade[subject_list]:
                    code = generate_code(stream, bulk_insert, subject, grade)
                    bulk_insert.append(
                        Subject(name=subject, grade_id=grade_id,
                                code=code, stream_id=streams[stream])
                    )
            continue  # Skip to next iteration after handling streams

        # Default handling for non-stream subjects
        for subject in subjects:
            code = generate_code(None, bulk_insert, subject, grade)
            bulk_insert.append(
                Subject(name=subject, grade_id=grade_id, code=code))

    session.bulk_save_objects(bulk_insert)
    session.commit()


def generate_code(stream, prev_data, subject, grade):
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
    base_code = "".join([word[:prefix_length].upper()
                        for word in words if word.isalpha() and word != 'and'])

    # Append the grade number to the base code
    base_code += str(grade)

    # Append the stream to the base code
    if stream:
        base_code += f'-{stream[0].upper()}'

    existing_codes = {subj.code for subj in prev_data}

    code = base_code
    suffix = '-I'

    while code in existing_codes:
        code = f"{base_code}{suffix}"
        suffix += 'I'

    return code


class Subject(BaseModel):
    """
    Subject Model

    This model represents a subject in the ClassEase system. It includes the subject's name, code, associated grade, and year.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        name (mapped_column): The name of the subject, limited to 50 characters, cannot be null.
        code (mapped_column): The code of the subject, limited to 10 characters, cannot be null.
        grade_id (mapped_column): Foreign key linking to the grade, cannot be null.
        year (mapped_column): The academic year of the subject, limited to 10 characters, cannot be null.

    Methods:
        __init__(*args, **kwargs): Initializes the subject with variable length arguments and keyword arguments.
    """
    __tablename__ = 'subjects'
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    code: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    grade_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('grades.id'), nullable=False)
    stream_id: Mapped[str] = mapped_column(String(120), ForeignKey(
        'streams.id'), nullable=True, default=None)
