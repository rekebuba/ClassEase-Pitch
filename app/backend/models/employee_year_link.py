import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from models.base.base_model import Base

if TYPE_CHECKING:
    pass


@dataclass
class EmployeeYearLink(Base):
    __tablename__ = "employee_year_links"

    employee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("employees.id", ondelete="CASCADE"),
        primary_key=True,
    )
    year_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("years.id", ondelete="CASCADE"),
        primary_key=True,
    )

    __table_args__ = (
        UniqueConstraint(
            "employee_id",
            "year_id",
            name="uq_employee_year_links",
        ),
    )
