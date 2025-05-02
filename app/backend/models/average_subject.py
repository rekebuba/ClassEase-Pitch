#!/usr/bin/python3
""" Module for Average Result class """

from sqlalchemy import String, Integer, ForeignKey, Float
from models.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship


class AVRGSubject(BaseModel):
    __tablename__ = 'average_subjects'
    user_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('users.id'), nullable=False)
    student_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('students.id'), nullable=False)
    subject_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('subjects.id'), nullable=False)
    year_record_id: Mapped[str] = mapped_column(String(120), ForeignKey(
        'student_year_records.id'), nullable=True)
    teachers_record_id: Mapped[str] = mapped_column(String(120), ForeignKey(
        'teachers_records.id', ondelete="SET NULL"), nullable=True, default=None)
    # The actual average score of the student in this for all subject
    average: Mapped[float] = mapped_column(Float, default=None)
    rank: Mapped[int] = mapped_column(Integer, default=None)

    # Relationships
    students = relationship("Student", back_populates='average_subjects')
