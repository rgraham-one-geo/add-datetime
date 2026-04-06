from datetime import datetime, timedelta

from add_datetime import add_datetime


def test_add_datetime() -> None:
    start = datetime(2026, 4, 5, 12, 0, 0)
    result = add_datetime(start, timedelta(hours=2, minutes=30))

    assert result == datetime(2026, 4, 5, 14, 30, 0)
