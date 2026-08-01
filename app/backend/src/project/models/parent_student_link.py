import uuid

from sqlalchemy import UUID, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from project.models.base.base_model import BaseModel


class ParentStudentLink(BaseModel):
    """
    Represents a link between a parent and a student in the database.
    This link is global (User to User).
    """

    __tablename__ = "parent_student_links"

    parent_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    student_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    __table_args__ = (
        UniqueConstraint(
            "parent_user_id",
            "student_user_id",
            name="uq_parent_student_links",
        ),
    )
