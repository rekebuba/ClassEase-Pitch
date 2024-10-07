#!/usr/bin/python3

from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, Float
from models.engine.db_storage import BaseModel, Base


class Student(BaseModel, Base):
    __tablename__ = 'students'
    first_name = Column(String(50), nullable=False)
    father_name = Column(String(50), nullable=False)
    g_father_name = Column(String(50))
    age = Column(Integer, nullable=False)
    password = Column(String(120))
    father_phone = Column(String(15))
    mother_phone = Column(String(15))

    grade_id = Column(String(120), ForeignKey('grades.id'), nullable=False)
    section_id = Column(String(120), ForeignKey('sections.id'))


    total_average = Column(Float, default=0)

    __table_args__ = (
        CheckConstraint(
            'father_phone IS NOT NULL OR mother_phone IS NOT NULL'),
    )

    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
