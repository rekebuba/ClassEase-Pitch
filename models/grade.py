#!/usr/bin/python3

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.engine.db_storage import BaseModel, Base


def seed_grades(session):
    """Populate the Grade table with default data (1 to 12)."""
    existing_grades = session.query(Grade).all()
    if not existing_grades:  # Only seed if table is empty
        for i in range(1, 13):
            grade = Grade(grade=i)
            session.add(grade)
        session.commit()


class Grade(BaseModel, Base):
    __tablename__ = 'grades'
    grade = Column(Integer, nullable=False, unique=True)

    # Define relationships
    section = relationship("Section", backref="grade",
                           cascade="all, delete-orphan")
    subject = relationship("Subject", backref="grade",
                           cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
