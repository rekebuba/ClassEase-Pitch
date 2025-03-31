#!/usr/bin/python3
""" Module for Assessment class """

from sqlalchemy import String, Integer, ForeignKey, Float
from models.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column


class Assessment(BaseModel):
    """
    This model represents an assessment record for a student, including details such as the student's ID, grade ID, subject ID, total score, rank, semester, and year.
    """
    __tablename__ = 'assessments'
    user_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('users.id'), nullable=False)
    semester_record_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('student_semester_records.id'), nullable=False)
    subject_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('subjects.id'), nullable=False)
    teachers_record_id: Mapped[str] = mapped_column(String(120), ForeignKey(
        'teachers_records.id', ondelete="SET NULL"), nullable=True, default=None)
    # The subject sum score of the student for each assessment
    total: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    rank: Mapped[int] = mapped_column(Integer, nullable=True, default=None)
