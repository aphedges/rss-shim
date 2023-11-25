"""General utilities to make programming easier."""

import datetime as dt


def now() -> dt.datetime:
    """Retrieve the current date and time."""
    # Always use UTC as time zone because `datetime.now()`
    # returns "naive" (non-TZ-aware) `datetime`s
    return dt.datetime.now(dt.UTC)
