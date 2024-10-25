
#!/usr/bin/python3

from sqlalchemy import Column, String, Integer, ForeignKey, Float
from models.engine.db_storage import BaseModel, Base

class Assessment(BaseModel, Base):
    __tablename__ = 'assessments'
    student_id = Column(String(120), ForeignKey('student.id'), nullable=False)
    grade_id = Column(String(120), ForeignKey('grades.id'), nullable=False)
    subject_id = Column(String(120), ForeignKey('subjects.id'), nullable=False)
    total = Column(Float, default=0)  # The sum score of the student for each assessment
    rank = Column(Integer)
    semester = Column(Integer, nullable=False)
    year = Column(String(10), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
