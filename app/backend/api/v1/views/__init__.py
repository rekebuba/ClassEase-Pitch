from flask import Blueprint

base_api = Blueprint("base_api", __name__, url_prefix="/api/v1")

from api.v1.views.academic_term.get import route # noqa: E402
