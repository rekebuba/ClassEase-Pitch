#!/usr/bin/python3
""" Module for Year class """

from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from models.engine.db_storage import BaseModel, Base
from datetime import datetime
from pyethiodate import EthDate


def seed_year(session):
    # Check if the table is already populated
    if session.query(Year).count() > 0:
        return

    ethiopian_year = current_EC_year()
    gregorian_year = current_GC_year(ethiopian_year)

    new_year = Year(ethiopian_year=ethiopian_year,
                    gregorian_year=gregorian_year)

    session.add(new_year)
    session.commit()


def current_EC_year() -> int:
    return EthDate.date_to_ethiopian(datetime.now()).year


def current_GC_year(ethiopian_year: int) -> str:
    return f'{ethiopian_year + 7}/{ethiopian_year + 8}'


class Year(BaseModel, Base):
    """docstring for year."""
    __tablename__ = 'years'
    ethiopian_year = Column(Integer, nullable=False, unique=True)
    gregorian_year = Column(String(15), default=None, nullable=True, unique=True)

    def __init__(self, *args, **kwargs):
        """ Initializes the registration instance. """
        super().__init__(*args, **kwargs)
