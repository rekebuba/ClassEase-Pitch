#!/usr/bin/python3

from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from models.engine.db_storage import BaseModel, Base


class Student(BaseModel, Base):
    __tablename__ = 'students'
    first_name = Column(String(50), nullable=False)
    father_name = Column(String(50), nullable=False)
    G_Father_name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)

    father_phone = Column(Integer)
    mother_phone = Column(Integer)
    guardian_phone = Column(Integer)

    

    grade_id = Column(String(60), ForeignKey('grades.id'), nullable=False)
    section_id = Column(String(60), ForeignKey('sections.id'))

    __table_args__ = (
        CheckConstraint(
            'father_phone IS NOT NULL OR mather_phone IS NOT NULL OR guardian_phone IS NOT NULL'),
    )

    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
