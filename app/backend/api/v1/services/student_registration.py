#!/usr/bin/python3
"""
This module contains the student registration function.
"""

from models import storage
from models.student import Student
from models.grade import Grade
from models.year import Year
from models.student_year_record import StudentYearRecord


def register_student(student_id: str, grade_id: str, year_id: str) -> None:
    """
    Registers a student for a specific grade and year.

    Args:
        student_id (str): The ID of the student to register.
        grade_id (str): The ID of the grade to register the student for.
        year_id (str): The ID of the year to register the student for.
    """
    student = storage.session.get(Student, student_id)
    grade = storage.session.get(Grade, grade_id)
    year = storage.session.get(Year, year_id)

    if not student or not grade or not year:
        raise ValueError("Invalid student, grade, or year ID.")

    student_grade_link = StudentYearRecord(
        student_id=student_id,
        grade_id=grade_id,
        year_id=year_id,
    )
    storage.new(student_grade_link)
    storage.save()
