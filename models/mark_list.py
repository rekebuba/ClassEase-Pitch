#!/usr/bin/python3

from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from models.engine.db_storage import BaseModel, Base


class MarkList(BaseModel, Base):
    __tablename__ = 'mark_lists'
    student_id = Column(String(120), ForeignKey('student.id'), nullable=False)
    grade_id = Column(String(120), ForeignKey('grades.id'), nullable=False)
    section_id = Column(String(120), ForeignKey('sections.id'))
    subject_id = Column(String(120), ForeignKey('subjects.id'), nullable=False)
    teachers_record_id = Column(String(120), ForeignKey('teachers_record.id', ondelete="SET NULL"), nullable=True, default=None)
    semester = Column(Integer, nullable=False)
    year = Column(String(10), nullable=False)
    type = Column(String(50), nullable=False)  # e.g., 'Test', 'Quiz', 'Assignment', 'Midterm', 'Final'
    percentage = Column(Float, nullable=False)  # percentage of this assessment towards the final score
    score = Column(Float)  # The actual score of the student in this assessment

    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
