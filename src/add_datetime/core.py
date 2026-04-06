from __future__ import annotations

from datetime import datetime, timedelta


def add_datetime(dt: datetime, delta: timedelta) -> datetime:
    """Return a new datetime offset by the given timedelta."""
    return dt + delta


def now_plus(delta: timedelta) -> datetime:
    """Return the current local datetime plus the given timedelta."""
    return datetime.now() + delta
