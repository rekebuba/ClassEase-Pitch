import uuid

from sqlalchemy import UUID, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from project.models.base.base_model import BaseModel


class ParentStudentLink(BaseModel):
    """
    Represents a link between a parent and a student in the database.
    """

    __tablename__ = "parent_student_links"

    parent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("parents.id", ondelete="CASCADE"),
        primary_key=True,
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("students.id", ondelete="CASCADE"),
        primary_key=True,
    )

    __table_args__ = (
        UniqueConstraint(
            "parent_id",
            "student_id",
            name="uq_parent_student_links",
        ),
    )
