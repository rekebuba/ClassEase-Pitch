from project.utils.type import FixtureConfig
from tests.fixtures import (
    ADMIN_PER_SCHOOL,
    EMPLOYEES_PER_SCHOOL,
    NUM_TEST_SCHOOLS,
    NUM_TEST_USERS,
    STUDENTS_PER_SCHOOL,
    YEARS_PER_SCHOOL,
)

FIXTURE_CONFIG: dict[str, FixtureConfig] = {
    "school": {"count": NUM_TEST_SCHOOLS, "id_prefix": "school"},
    "user": {"count": NUM_TEST_USERS, "id_prefix": "user"},
    "admin": {"count": NUM_TEST_SCHOOLS * ADMIN_PER_SCHOOL, "id_prefix": "admin"},
    "student": {
        "count": NUM_TEST_SCHOOLS * STUDENTS_PER_SCHOOL,
        "id_prefix": "student",
    },
    "employee": {
        "count": NUM_TEST_SCHOOLS * EMPLOYEES_PER_SCHOOL,
        "id_prefix": "employee",
    },
    "year": {"count": NUM_TEST_SCHOOLS * YEARS_PER_SCHOOL, "id_prefix": "year"},
    "grade": {"count": NUM_TEST_SCHOOLS, "id_prefix": "grade"},
    # add new entities here
}


def pytest_generate_tests(metafunc):
    for fixture_name, config in FIXTURE_CONFIG.items():
        if fixture_name in metafunc.fixturenames:
            metafunc.parametrize(
                fixture_name,
                range(config["count"]),
                indirect=True,
                ids=[f"{config['id_prefix']}_{i}" for i in range(config["count"])],
            )
