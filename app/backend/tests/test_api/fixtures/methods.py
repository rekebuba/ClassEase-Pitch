from typing import Any, Dict, List, Sequence, Tuple

from flask.testing import FlaskClient
import pytest
from sqlalchemy import select

from api.v1.views.shared.auth.schema import AuthResponseSchema
from extension.pydantic.response.schema import SuccessResponseSchema
from models.user import User
from sqlalchemy.orm import scoped_session, Session

from tests.typing import Credential


@pytest.fixture
def role(
    request: pytest.FixtureRequest, db_session: scoped_session[Session]
) -> Sequence[User]:
    """
    Fixture to get a user based on role and count.
    """
    role, count = request.param
    user = db_session.scalars(select(User).filter(User.role == role).limit(count)).all()

    return user


def prepare_form_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively flatten nested dictionary into form-compatible format
    and separate files for multipart form upload.
    """
    form_data = {}

    for key, value in data.items():
        if isinstance(value, dict):
            # Handle nested dictionaries by flattening keys (e.g., {"user": {"name": "John"}} becomes "user.name")
            for sub_key, sub_value in value.items():
                nested_key = f"{key}.{sub_key}"
                form_data[nested_key] = sub_value
        else:
            form_data[key] = value

    return form_data


def is_table_sorted(columns_info: List[Tuple[List[Any], bool]]) -> bool:
    """
    Checks whether a table is sorted according to multi-column sort orders.

    The parameter is a list of tuples (column, descending) where:
      - 'column' is an ordered sequence representing the values in that column.
      - 'descending' is a boolean: when True, the column must be in descending order;
        when False, the column must be in ascending order.

    The table’s rows are constructed by taking the ith element from each column. To decide
    whether row i and row i+1 are in correct order, we compare them column by column:
      - If the values are equal, the decision falls to the next column.
      - If they differ, the decision is based on the sort order defined in that column:
          * Ascending (False): value_i should be <= value_i+1
          * Descending (True): value_i should be >= value_i+1

    Raises:
      ValueError: If not all columns have the same number of elements.

    Returns:
      bool: True if every adjacent row is in order; otherwise, False.
    """
    # Return True immediately if there are no columns.
    if not columns_info:
        return True

    # Determine the number of rows and verify that each column has the expected length.
    first_column, _ = columns_info[0]
    num_rows = len(first_column)
    for column, _ in columns_info:
        if len(column) != num_rows:
            raise ValueError("All columns must have the same number of rows.")

    next_column = True
    # Compare each adjacent pair of rows.
    for i in range(num_rows - 1):
        if not next_column:
            break  # If we already found a column that determines the order, we can stop checking.

        next_column = False
        # Iterate through the columns in order.
        for column, descending in columns_info:
            current_val = column[i]
            next_val = column[i + 1]

            # If Any of the values are None, treat them as less than any other value.
            if current_val is None or next_val is None:
                continue

            # If they are equal, move to the next column.
            if current_val == next_val:
                next_column = True  # if the current column is equal, we need to check the next column
                continue

            # For ascending order, the current value must be less than or equal to the next.
            if not descending:
                if current_val > next_val:
                    return False
                else:
                    # Since this column decided the order, we can stop checking further columns.
                    break
            # For descending order, the current value must be greater than or equal to the next.
            else:
                if current_val < next_val:
                    return False
                else:
                    break
    return True


def get_auth_header(
    client: FlaskClient,
    identification: str,
    password: str,
) -> Credential:
    """
    Authenticate a user and return the authorization header.

    Args:
        client: The Flask test client.
        identification: The identification of the user to authenticate.
        password: The password of the user to authenticate.

    Returns:
        A dictionary containing the authorization header.
    """
    response = client.post(
        "/api/v1/auth/login",
        json={"identification": identification, "password": password},
    )
    assert response.status_code == 200, "Authentication failed"
    assert response.json is not None
    try:
        valid_response = SuccessResponseSchema[
            AuthResponseSchema, None, None
        ].model_validate(response.json)
    except Exception as e:
        pytest.fail(f"Response validation failed: {str(e)}")

    token = valid_response.data.api_key
    if not token:
        pytest.fail("Authentication token is missing in the response")

    return {"header": {"apiKey": f"Bearer {token}"}}
