# #!/usr/bin/python3

# from sqlalchemy import Column, Integer, String, ForeignKey
# from models.engine.db_storage import BaseModel, Base


# class Grade(BaseModel, Base):
#     __tablename__ = 'grade'
#     user_id = Column(String(60), ForeignKey('user.id'), nullable=False)
#     class_id = Column(String(60), ForeignKey('classes.id'), nullable=False)
#     grade = Column(String(2), nullable=False)

#     def __init__(self, *args, **kwargs):
#         """initializes score"""
#         super().__init__(*args, **kwargs)
