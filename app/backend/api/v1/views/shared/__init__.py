from flask import Blueprint


auths = Blueprint("auths", __name__, url_prefix="/api/v1")


from api.v1.views.shared.auth import route  # noqa: E402
from api.v1.views.shared.registration import route  # noqa: E402
from api.v1.views.shared.dashboard import route  # noqa: E402
from api.v1.views.shared.grades import route  # noqa: E402
from api.v1.views.shared.subjects import route  # noqa: E402
from api.v1.views.shared.year import route  # noqa: E402
from api.v1.views.shared.section import route  # noqa: E402
from api.v1.views.shared.stream import route  # noqa: E402
