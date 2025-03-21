#!/usr/bin/python3
""" Module for Subject class """

from sqlalchemy import CheckConstraint, Integer, String, ForeignKey
from models.grade import Grade
from models.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column


def seed_streams(session):
    """
    Populate the Stream table with default data.

    This function checks if the Stream table is empty. If it is, it populates
    the table with streams 'natural' and 'social'. If the table already contains
    data, the function does nothing.

    Args:
        session (Session): SQLAlchemy session object used to interact with the database.

    """
    # Check if the table is already populated
    if session.query(Stream).count() > 0:
        return

    streams = ['natural', 'social']
    for stream in streams:
        stream_instance = Stream(name=stream)
        session.add(stream_instance)
    session.commit()


class Stream(BaseModel):
    __tablename__ = 'streams'

    name: Mapped[str] = mapped_column(String(10), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "name IN ('natural', 'social')",
            name="check_stream"
        ),
    )
