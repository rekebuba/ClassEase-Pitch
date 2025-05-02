#!/usr/bin/python3
""" Module for Average Result class """

from sqlalchemy import String, Integer, ForeignKey, Float
from models.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship


class STUDSemesterRecord(BaseModel):
    """
    This model represents the average result of a student for a particular semester and year.
    """
    __tablename__ = 'student_semester_records'
    student_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('students.id'), nullable=False)
    semester_id: Mapped[str] = mapped_column(String(120), ForeignKey(
        'semesters.id'), nullable=False)
    section_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('sections.id'), nullable=False)
    year_record_id: Mapped[str] = mapped_column(String(120), ForeignKey(
        'student_year_records.id'), nullable=True, default=None)
    average: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    rank: Mapped[int] = mapped_column(Integer, nullable=True, default=None)

    # Relationships
    students = relationship("Student", back_populates='semester_records')
    year_records = relationship(
        "STUDYearRecord", back_populates='semester_records')
    semesters = relationship("Semester", back_populates='semester_records')
    sections = relationship("Section", back_populates='semester_records')
