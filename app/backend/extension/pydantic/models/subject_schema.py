from __future__ import annotations
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from flask import url_for
from pydantic import BaseModel, ConfigDict, Field

from api.v1.views.utils import generate_token
from extension.functions.helper import to_camel
from extension.pydantic.hal_link.link_schema import Link
from models.subject import Subject

if TYPE_CHECKING:
    from .teacher_schema import TeacherSchema
    from .yearly_subject_schema import YearlySubjectSchema


class SubjectSchema(BaseModel):
    """
    This model represents a subject in the system. It inherits from BaseModel.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    name: str
    links: Dict[str, Link] = Field(alias="_links")

    @classmethod
    @generate_token
    def hal_form(cls, Subject: Subject, token: str) -> Dict[str, Any]:
        links = {
            "self": Link(
                href=url_for("auths.get_subject_by_id", subject_id=token),
                method="GET",
            )
        }

        setattr(Subject, "_links", links)
        base_model = cls.model_validate(Subject).model_dump(by_alias=True)

        return base_model


class SubjectRelationshipSchema(BaseModel):
    """This model represents the relationships of a SubjectSchema.
    It is used to define the relationships between the SubjectSchema and other schemas.
    """

    teachers: Optional[List[TeacherSchema]]
    yearly_subjects: Optional[List[YearlySubjectSchema]]
