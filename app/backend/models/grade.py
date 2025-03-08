#!/usr/bin/python3
""" Module for Grade class """

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.engine.db_storage import BaseModel, Base


def seed_grades(session):
    """
    Populate the Grade table with default data (grades 1 to 12).

    This function checks if the Grade table is empty. If it is, it populates
    the table with grades from 1 to 12. If the table already contains data,
    the function does nothing.

    Args:
        session (Session): SQLAlchemy session object used to interact with the database.

    """
    existing_grades = session.query(Grade).all()
    if not existing_grades:  # Only seed if table is empty
        for i in range(1, 13):
            grade = Grade(name=i)
            session.add(grade)

        session.commit()


class Grade(BaseModel, Base):
    """
    Grade Model

    This model represents the 'grades' table in the database and includes the following attributes and relationships:

    Attributes:
        grade (int): The grade value, which is an integer and must be unique and not null.

    Relationships:
        section (relationship): A one-to-many relationship with the Section model. If a grade is deleted, all associated sections are also deleted.
        subject (relationship): A one-to-many relationship with the Subject model. If a grade is deleted, all associated subjects are also deleted.

    Methods:
        __init__(*args, **kwargs): Initializes a new instance of the Grade model.
    """
    __tablename__ = 'grades'
    name = Column(Integer, nullable=False, unique=True)

    # Define relationships
    section = relationship("Section", backref="grade",
                           cascade="all, delete-orphan")
    subject = relationship("Subject", backref="grade",
                           cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """
        Initializes the score.

        Parameters:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
