from typing import Tuple
from flask import Response, jsonify
from pydantic import ValidationError
from api.v1.utils.typing import UserT
from api.v1.views import errors
from api.v1.views.shared import auths as auth
from api.v1.views.utils import student_teacher_or_admin_required
from extension.pydantic.models.user_schema import UserWithRelationshipsSchema


@auth.route("/", methods=["GET"])
@student_teacher_or_admin_required
def user(user: UserT) -> Tuple[Response, int]:
    try:
        user_schema = UserWithRelationshipsSchema.model_validate(user)
        return jsonify(
            user_schema.model_dump(by_alias=True, exclude_none=True, mode="json")
        ), 200

    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)
