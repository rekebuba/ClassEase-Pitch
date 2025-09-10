#!/usr/bin/python3
"""Module for SavedQueryView class"""

import uuid
from typing import TYPE_CHECKING, Any, Dict

from sqlalchemy import JSON, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base.base_model import BaseModel
from models.base.column_type import UUIDType
from utils.enum import TableEnum

if TYPE_CHECKING:
    from models.user import User


class SavedQueryView(BaseModel):
    """Model for saved queries associated with a user."""

    __tablename__ = "saved_query_views"

    # Columns
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    table_name: Mapped[TableEnum] = mapped_column(
        Enum(
            TableEnum,
            name="table_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )
    query_json: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(
        "User", back_populates="saved_query_views", init=False
    )
