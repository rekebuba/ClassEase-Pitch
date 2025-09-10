from unittest.mock import MagicMock, patch

from sqlalchemy import text

from tests_pre_start import init, logger


def test_init_successful_connection() -> None:
    engine_mock = MagicMock()

    session_mock = MagicMock()
    execute_mock = MagicMock(return_value=True)
    session_mock.configure_mock(**{"execute_mock.return_value": execute_mock})

    with (
        patch("sqlalchemy.orm.Session", return_value=session_mock),
        patch.object(logger, "info"),
        patch.object(logger, "error"),
        patch.object(logger, "warn"),
    ):
        try:
            init(engine_mock)
            connection_successful = True
        except Exception:
            connection_successful = False

        assert connection_successful, (
            "The database connection should be successful and not raise an exception."
        )

        assert session_mock.execute.called_once_with(text("SELECT 1")), (
            "The session should execute a select statement once."
        )
