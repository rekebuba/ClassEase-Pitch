from typing import Tuple
from flask import Response, jsonify
from pydantic import ValidationError
from sqlalchemy import select
from api.v1.utils.typing import UserT
from api.v1.views import errors
from api.v1.views.shared import auths as auth
from api.v1.views.utils import student_teacher_or_admin_required
from extension.pydantic.models.section_schema import SectionSchema
from models import storage
from models.section import Section
# noqa: E402

@auth.route("/sections", methods=["GET"])
@student_teacher_or_admin_required
def get_sections(user: UserT) -> Tuple[Response, int]:
    """
    Get all sections.

    Returns:
        Tuple[Response, int]: JSON response with sections and status code.
    """
    try:
        sections = storage.session.scalars(select(Section)).all()
        sections_schema = [
            SectionSchema.model_validate(section) for section in sections
        ]
        response = [
            section_schema.model_dump(by_alias=True, exclude_none=True)
            for section_schema in sections_schema
        ]
        return jsonify(response), 200

    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)


@auth.route("/sections/<string:section_id>", methods=["GET"])
@student_teacher_or_admin_required
def get_section_by_id(user: UserT, section_id: str) -> Tuple[Response, int]:
    """
    Get a section by its ID.

    Args:
        section_id (str): The ID of the section.

    """
    try:
        section = storage.session.get(Section, section_id)
        if not section:
            return errors.handle_not_found_error("Section not found")

        section_schema = SectionSchema.model_validate(section)
        return jsonify(section_schema.model_dump(by_alias=True, exclude_none=True)), 200

    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)
