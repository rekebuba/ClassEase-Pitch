# #!/usr/bin/python3

# from sqlalchemy import Column, Integer, String, ForeignKey
# from models.engine.db_storage import BaseModel, Base

# class Teacher(BaseModel, Base):
#     __tablename__ = 'teachers'
#     name = Column(String(50), nullable=False)
#     subject_id = Column(Integer, ForeignKey('subjects.id'))
#     grade = Column(Integer, nullable=False)

#     def __init__(self, *args, **kwargs):
#         """initializes score"""
#         super().__init__(*args, **kwargs)
