#!/usr/bin/python3
from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, Float, DateTime
from models.engine.db_storage import BaseModel, Base


class StudentYearlyRecord(BaseModel, Base):
    __tablename__ = 'student_yearly_records'
    student_id = Column(String(120), ForeignKey('student.id'), nullable=False)
    year = Column(String(10), nullable=False)
    grade_id = Column(String(120), ForeignKey('grades.id'), nullable=False)
    section_id = Column(String(120), ForeignKey('sections.id'), nullable=True)
    final_score = Column(Float, nullable=True, default=None)  # year-end score
    rank = Column(Integer, nullable=True, default=None)


    # Relationship to Student
    # student = relationship("Student", backref="yearly_records")


    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
