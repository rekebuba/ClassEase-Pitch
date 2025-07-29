from typing import Tuple
from flask import Response
from api.v1.utils.typing import UserT
from api.v1.views.admin import admins as admin
from api.v1.views.utils import admin_required


@admin.route("academic_year/setup", methods=["POST"])
@admin_required
def set_up_academic_year(user: UserT) -> Tuple[Response, int]:
    """"""
    pass

