from flask import Blueprint

admins = Blueprint("admins", __name__, url_prefix="/api/v1/admin")


from api.v1.views.admin.assign_teacher import route  # noqa: E402
from api.v1.views.admin.event import route  # noqa: E402
from api.v1.views.admin.mark_list import route  # noqa: E402
from api.v1.views.admin.overview import route  # noqa: E402
from api.v1.views.admin.profile import route  # noqa: E402
from api.v1.views.admin.registered_grade import route  # noqa: E402
from api.v1.views.admin.students.query import route  # noqa: E402
from api.v1.views.admin.students.average_range import route
from api.v1.views.admin.students.grade_count import route
from api.v1.views.admin.students.mark_list import route
from api.v1.views.admin.students.section_count import route
from api.v1.views.admin.students.status_count import route
from api.v1.views.admin.students.views import route


from api.v1.views.admin.teacher import route  # noqa: E402
