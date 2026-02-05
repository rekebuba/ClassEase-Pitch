from unittest.mock import MagicMock, patch

from tests_pre_start import init, logger


def test_init_successful_connection() -> None:
    engine_mock = MagicMock()

    connection_mock = MagicMock()
    # This chain simulates: with engine.connect() as conn:
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

        assert connection_successful, (
            "The database connection should be successful and not raise an exception."
        )

        # 3. Verify the call happened exactly once
        assert connection_mock.execute.call_count == 1, (
            "The connection should execute a statement once."
        )

        # We grab the arguments from the call and check the string value.
        args, _ = connection_mock.execute.call_args
        assert str(args[0]) == "SELECT 1"
