import uuid
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlalchemy import JSON, UUID, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel

if TYPE_CHECKING:
    from project.models.employment_application import EmploymentApplication
    from project.models.user import User


class EmploymentProfile(BaseModel):
    __tablename__ = "employment_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    city: Mapped[str] = mapped_column(String(80), nullable=False)
    highest_education: Mapped[str] = mapped_column(String(120), nullable=False)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)
    field_of_study: Mapped[Optional[str]] = mapped_column(String(120), nullable=True, default=None)
    institution: Mapped[Optional[str]] = mapped_column(String(160), nullable=True, default=None)
    years_of_experience: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=None)
    skills: Mapped[List[str]] = mapped_column(JSON, nullable=False, default_factory=list)
    certifications: Mapped[List[str]] = mapped_column(JSON, nullable=False, default_factory=list)
    extra: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default_factory=dict)

    __table_args__ = (UniqueConstraint("user_id", name="uq_employment_profile_user"),)

    user: Mapped["User"] = relationship(
        "User",
        back_populates="employment_profile",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    applications: Mapped[List["EmploymentApplication"]] = relationship(
        "EmploymentApplication",
        back_populates="profile",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    @property
    def is_complete(self) -> bool:
        required = [self.city, self.highest_education, self.field_of_study, self.institution]
        return all(bool(field) for field in required)
