#!/usr/bin/python3
""" Module for Grade class """

from dataclasses import dataclass, field
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, MappedAsDataclass
from models.base_model import BaseModel


def seed_grades(session):
    """
    Populate the Grade table with default data (grades 1 to 12).

    This function checks if the Grade table is empty. If it is, it populates
    the table with grades from 1 to 12. If the table already contains data,
    the function does nothing.

    Args:
        session (Session): SQLAlchemy session object used to interact with the database.

    """
    # Check if the table is already populated
    if session.query(Grade).count() > 0:
        return

    for i in range(1, 13):
        grade = Grade(name=i)
        session.add(grade)

    session.commit()


class Grade(BaseModel):
    """Grade Model"""

    __tablename__ = "grades"

    # Database column
    name: Mapped[int] = mapped_column(
        Integer, unique=True, nullable=False, index=True)
