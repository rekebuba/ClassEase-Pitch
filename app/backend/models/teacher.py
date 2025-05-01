#!/usr/bin/python3
""" Module for Teacher class """

from sqlalchemy import CheckConstraint, Date, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel


class Teacher(BaseModel):
    """
    This model represents a teacher in the ClassEase system. It inherits from BaseModel and Base.
    """
    __tablename__ = 'teachers'
    user_id: Mapped[str] = mapped_column(String(120), ForeignKey(
        'users.id'), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    father_name: Mapped[str] = mapped_column(String(50), nullable=False)
    grand_father_name: Mapped[str] = mapped_column(String(50), nullable=False)
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(1), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(25), nullable=False)
    address: Mapped[str] = mapped_column(String(120), nullable=False)
    year_of_experience: Mapped[int] = mapped_column(Integer, nullable=False)
    qualification: Mapped[str] = mapped_column(String(120), nullable=False)

    user = relationship('User', back_populates='teacher')

    __table_args__ = (
        CheckConstraint(
            "gender IN ('M', 'F')",
            name="check_teacher_gender"
        ),
        CheckConstraint(
            "year_of_experience >= 0",
            name="check_teacher_experience"
        )
    )
