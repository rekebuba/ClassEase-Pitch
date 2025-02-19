#!/usr/bin/python3
""" Module for Section class """

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.engine.db_storage import BaseModel, Base


class Section(BaseModel, Base):
    """
    Section Model

    Represents a section within a grade.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        section (Column): The section identifier (e.g., A, B, C, D, E, F, G).
        grade_id (Column): Foreign key linking to the grades table.

    Methods:
        __init__(*args, **kwargs): Initializes the section instance.
    """
    __tablename__ = 'sections'
    section = Column(String(1))  # e.g., A, B, C, D, E, F, G
    grade_id = Column(String(120), ForeignKey('grades.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        """
        Initializes the score.

        Parameters:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
