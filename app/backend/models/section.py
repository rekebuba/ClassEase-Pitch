#!/usr/bin/python3
""" Module for Section class """

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel


class Section(BaseModel):
    """
    Section Model

    Represents a section within a grade.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        section (mapped_column): The section identifier (e.g., A, B, C, D, E, F, G).
        grade_id (mapped_column): Foreign key linking to the grades table.

    Methods:
        __init__(*args, **kwargs): Initializes the section instance.
    """
    __tablename__ = 'sections'
    section: Mapped[str] = mapped_column(
        String(1))  # e.g., A, B, C, D, E, F, G
    grade_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('grades.id'), nullable=False)
    semester_id: Mapped[str] = mapped_column(String(120), ForeignKey(
        'semesters.id'), nullable=False)
