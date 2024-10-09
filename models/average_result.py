#!/usr/bin/python3

from sqlalchemy import Column, String, Integer, ForeignKey, Float
from models.engine.db_storage import BaseModel, Base

class AVRGResult(BaseModel, Base):
    __tablename__ = 'average_result'
    student_id = Column(String(120), ForeignKey('student.id'), nullable=False)
    average = Column(Float, default=0)  # The actual score of the student in this assessment
    semester = Column(Integer, nullable=False)
    school_year = Column(String(10), nullable=False)
    rank = Column(Integer)

    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
