#!/usr/bin/python3
""" Module for Admin class """

from sqlalchemy import CheckConstraint, Date, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel


class Admin(BaseModel):
    """
    Admin Model

    This model represents an admin in the system. It inherits from BaseModel and Base.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        id (str): The unique identifier for the admin, which is a foreign key referencing the users table.
        name (str): The name of the admin. This field is required.
        email (str): The email of the admin. This field is required and must be unique.

    Methods:
        __init__(*args, **kwargs): Initializes the admin instance.
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

