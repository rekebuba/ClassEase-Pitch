from flask import Blueprint


auths = Blueprint("auths", __name__, url_prefix="/api/v1/auth")


from api.v1.views.shared.auth import route  # noqa: E402
