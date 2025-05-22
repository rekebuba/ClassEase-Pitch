from flask import Blueprint


stud = Blueprint("stud", __name__, url_prefix="/api/v1/student")

from api.v1.views.student.yearly_score import route  # noqa: E402
from api.v1.views.student.course import route  # noqa: E402
from api.v1.views.student.profile import route  # noqa: E402
from api.v1.views.student.score import route  # noqa: E402
from api.v1.views.student.assigned_grade import route  # noqa: E402
