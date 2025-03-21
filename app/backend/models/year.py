#!/usr/bin/python3
""" Module for Year class """

from sqlalchemy import String, Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel
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


class Year(BaseModel):
    """docstring for year."""
    __tablename__ = 'years'
    ethiopian_year: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True)
    gregorian_year: Mapped[str] = mapped_column(
        String(15), default=None, nullable=True, unique=True)
