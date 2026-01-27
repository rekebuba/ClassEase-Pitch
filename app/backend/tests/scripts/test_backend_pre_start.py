from unittest.mock import MagicMock, patch

from sqlalchemy import text

from tests_pre_start import init, logger


def test_init_successful_connection() -> None:
    engine_mock = MagicMock()
    
    #    structure: engine.connect() -> __enter__() -> connection
    connection_mock = MagicMock()
    engine_mock.connect.return_value.__enter__.return_value = connection_mock

    with (
        patch.object(logger, "info"),
        patch.object(logger, "error"),
        patch.object(logger, "warn"),
    ):
        try:
            init(engine_mock)
            connection_successful = True
        except Exception:
            connection_successful = False

        assert connection_successful, "The database connection should be successful."

        #    This avoids issues where text("A") != text("A") in mocks
        assert connection_mock.execute.call_count == 1
        
        # Extract the first argument of the first call
        args, _ = connection_mock.execute.call_args
        executed_sql = args[0]
        
        # Verify the string representation of the SQL command matches
        assert str(executed_sql) == "SELECT 1"
