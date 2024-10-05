# #!/usr/bin/python3

# from sqlalchemy import Column, Integer, String, ForeignKey
# from models.engine.db_storage import BaseModel, Base


# class Subject(BaseModel, Base):
#     __tablename__ = 'subjects'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50), nullable=False)
#     teacher_id = Column(Integer, ForeignKey('teachers.id'))

#     def __init__(self, *args, **kwargs):
#         """initializes score"""
#         super().__init__(*args, **kwargs)
