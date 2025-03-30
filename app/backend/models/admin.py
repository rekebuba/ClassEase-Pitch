#!/usr/bin/python3
""" Module for Admin class """

from sqlalchemy import CheckConstraint, Date, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel


class Admin(BaseModel):
    """
    This model represents an admin in the system. It inherits from BaseModel and Base.
    """
    __tablename__ = 'admins'
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

    user = relationship('User', back_populates='admin')

    __table_args__ = (
        CheckConstraint(
            "gender IN ('M', 'F')",
            name="check_admin_gender"
        ),
    )
