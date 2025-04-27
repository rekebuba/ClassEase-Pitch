#!/usr/bin/python3
""" Module for Table class """
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from models.base_model import BaseModel
from sqlalchemy import inspect


def seed_table(session, engine):
    inspector = inspect(engine)
    db_tables = inspector.get_table_names()

    # Get names already in your 'tables' model
    existing_tables = {t.name for t in session.query(Table).all()}

    for table_name in db_tables:
        if table_name == 'tables':
            continue
        if table_name in existing_tables:
            continue

        new_table = Table(name=table_name)
        session.add(new_table)

    session.commit()


class Table(BaseModel):
    """docstring for table."""
    __tablename__ = 'tables'
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
