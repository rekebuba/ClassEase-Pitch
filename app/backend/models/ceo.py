#!/usr/bin/python3
"""Module for CEO class"""

import os
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, scoped_session, Session
from models.base.base_model import BaseModel


def seed_ceo(session: scoped_session[Session]) -> None:
    """create The first CEO When the database starts new"""
    if session.query(CEO).count() > 0:
        return

    username = os.getenv("CEO_USERNAME")
    password = os.getenv("CEO_PASSWORD")

    if not username or not password:
        raise ValueError

    new_ceo = CEO(username=username, password=password)

    session.add(new_ceo)
    session.commit()


class CEO(BaseModel):
    """
    This module defines the CEO model which represents a CEO in the system. The CEO can have one of three roles: 'admin', 'teacher', or 'student'. Each CEO has a unique ID and a password.
    """

    __tablename__ = "ceo"
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
