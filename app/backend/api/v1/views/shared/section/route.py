from typing import Set, Tuple
import uuid
from flask import Response
from pydantic import ValidationError
from sqlalchemy import select
from api.v1.utils.parameter import validate_fields
from api.v1.utils.typing import UserT
from api.v1.views import errors
from api.v1.views.shared import auths as auth
from api.v1.views.utils import student_teacher_or_admin_required
from extension.pydantic.models.section_schema import SectionSchema
from extension.pydantic.response.schema import success_response
from models import storage
from models.section import Section


@auth.route("/years/<uuid:year_id>/sections", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(SectionSchema, SectionSchema.default_fields())
def get_sections(
    user: UserT, fields: Set[str], year_id: uuid.UUID
) -> Tuple[Response, int]:
    """
    Get all sections.

    Returns:
        Tuple[Response, int]: JSON response with sections and status code.
    """
    try:
        sections = storage.session.scalars(
            select(Section).where(Section.year_id == year_id)
        ).all()

        sections_schema = [
            SectionSchema.model_validate(section) for section in sections
        ]
        response = [
            section_schema.model_dump(
                by_alias=True,
                exclude_none=True,
                include=fields,
                mode="json",
            )
            for section_schema in sections_schema
        ]

        return success_response(data=response)

    except ValidationError as e:
        return errors.handle_validation_error(error=e)
    except Exception as e:
        return errors.handle_internal_error(error=e)


@auth.route("/years/<uuid:year_id>/sections/<uuid:section_id>", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(SectionSchema, SectionSchema.default_fields())
def get_section_by_id(
    user: UserT,
    fields: Set[str],
    year_id: uuid.UUID,
    section_id: uuid.UUID,
) -> Tuple[Response, int]:
    """
    Get a section by its ID.

    Args:
        section_id (str): The ID of the section.

    """
    try:
        section = storage.session.scalar(
            select(Section).where(Section.id == section_id, Section.year_id == year_id)
        )
        if not section:
            return errors.handle_not_found_error(message="Section not found")

        section_schema = SectionSchema.model_validate(section)
        section_response = section_schema.model_dump(
            by_alias=True,
            exclude_none=True,
            include=fields,
            mode="json",
        )

        return success_response(data=section_response)

    except ValidationError as e:
        return errors.handle_validation_error(error=e)
    except Exception as e:
        return errors.handle_internal_error(error=e)
