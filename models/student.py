#!/usr/bin/python3
from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, Float, DateTime
from models.engine.db_storage import BaseModel, Base


class Student(BaseModel, Base):
    __tablename__ = 'student'
    id = Column(String(120), ForeignKey('users.id'), primary_key=True, unique=True)
    name = Column(String(50), nullable=False)
    father_name = Column(String(50), nullable=False)
    grand_father_name = Column(String(50))
    date_of_birth = Column(DateTime, nullable=False)
    father_phone = Column(String(25))
    mother_phone = Column(String(25))

    start_year = Column(String(10), nullable=False)
    end_year = Column(String(10))

    __table_args__ = (
        CheckConstraint(
            'father_phone IS NOT NULL OR mother_phone IS NOT NULL'),
    )


    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
