#!/usr/bin/python3
"""
This module contains the student promotion function.
"""

from models import storage
from models.student import Student
from models.grade import Grade
from models.year import Year
from models.student_year_record import StudentYearRecord


def promote_student(student_id: str, current_year_id: str, next_year_id: str) -> None:
    """
    Promotes a student to the next grade for the next academic year.

    Args:
        student_id (str): The ID of the student to promote.
        current_year_id (str): The ID of the current academic year.
        next_year_id (str): The ID of the next academic year.
    """
    student = storage.session.get(Student, student_id)
    current_year = storage.session.get(Year, current_year_id)
    next_year = storage.session.get(Year, next_year_id)

    if not student or not current_year or not next_year:
        raise ValueError("Invalid student or year ID.")

    # Find the student's current grade
    student_year_record = (
        storage.session.query(StudentYearRecord)
        .filter_by(student_id=student_id, year_id=current_year_id)
        .first()
    )

    if not student_year_record:
        raise ValueError("Student is not registered for the current year.")

    current_grade = storage.session.get(Grade, student_year_record.grade_id)

    if not current_grade:
        raise ValueError("Current grade does not exist.")

    # Determine the next grade
    next_grade_number = current_grade.grade + 1
    next_grade = storage.session.query(Grade).filter_by(grade=next_grade_number).first()

    if not next_grade:
        raise ValueError("Next grade does not exist.")

    # Create a new registration for the next grade and year
    new_grade_link = StudentYearRecord(
        student_id=student_id,
        grade_id=next_grade.id,
        year_id=next_year_id,
    )
    storage.new(new_grade_link)
    storage.save()
