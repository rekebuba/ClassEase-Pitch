from typing import Any, Dict

import pytest
from models.base_model import CustomTypes
from models.user import User


all_params: Dict[str, Any] = {
    "test_users_log_in_success": {
        "params": "role",
        "values": [
            (CustomTypes.RoleEnum.ADMIN, 1),
            (CustomTypes.RoleEnum.TEACHER, 1),
            (CustomTypes.RoleEnum.STUDENT, 1),
        ],
        "ids": ["Admin", "Teacher", "Student"],
    },
}


def pytest_generate_tests(metafunc):
    fct_name = metafunc.function.__name__
    if fct_name in all_params:
        params = all_params[fct_name]
        print("FUNCTION NAME:", fct_name)
        print("PARAMS:", params)
        metafunc.parametrize(
            params["params"],
            params["values"],
            ids=params["ids"],
            indirect=True,
        )


@pytest.fixture
def role(request, db_session):
    """
    Fixture to get a user based on role and count.
    """
    role, count = request.param
    user = db_session.query(User).filter(User.role == role).limit(count).all()

    return user
