#!/usr/bin/python3
""" Module for Section class """

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel


class Section(BaseModel):
    """
    Represents a section within a grade.
    """
    __tablename__ = 'sections'
    section: Mapped[str] = mapped_column(
        String(1))  # e.g., A, B, C, D, E, F, G
    grade_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('grades.id'), nullable=False)
    semester_id: Mapped[str] = mapped_column(String(120), ForeignKey(
        'semesters.id'), nullable=False)
