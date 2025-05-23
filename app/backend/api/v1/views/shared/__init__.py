from flask import Blueprint


auths = Blueprint("auths", __name__, url_prefix="/api/v1")


from api.v1.views.shared.auth import route  # noqa: E402
from api.v1.views.shared.registration import route  # noqa: E402
