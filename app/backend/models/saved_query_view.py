#!/usr/bin/python3
"""Module for SavedQueryView class"""

from typing import Any, Dict
from sqlalchemy import JSON, Enum, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel


class SavedQueryView(BaseModel):
    """Model for saved queries associated with a user."""

    __tablename__ = "saved_query_views"

    # Columns
    user_id: Mapped[str] = mapped_column(
        String(126), ForeignKey("users.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    table_name: Mapped[BaseModel.TableEnum] = mapped_column(
        Enum(BaseModel.TableEnum), nullable=False
    )
    query_json: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)

    # Relationships
    user = relationship("User", back_populates="saved_query_views")
