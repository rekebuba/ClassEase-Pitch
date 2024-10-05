# #!/usr/bin/python3

# from sqlalchemy import Column, Integer, String, Boolean
# from models.engine.db_storage import BaseModel, Base

# class Staff(BaseModel, Base):
#     __tablename__ = 'staff'
#     name = Column(String(50), nullable=False)
#     role = Column(String(50), nullable=False)  # e.g., Principal, System Admin
#     can_authorize = Column(Boolean, default=False)

#     def __init__(self, *args, **kwargs):
#         """initializes score"""
#         super().__init__(*args, **kwargs)
