"""Module to take the current date and yesterday's date in UTC timezone."""

from datetime import datetime, timedelta

import pytz


class TakeDate:
    """Class to get current date and yesterday's date in UTC timezone."""

    def __init__(self) -> None:
        """Initialize to set current and yesterday's date in UTC timezone."""
        UTC = self.timezone = pytz.timezone("UTC")
        self.now = datetime.now(UTC)
        self.yesterday = self.now - timedelta(days=1)
        self.yesterday_str = self.yesterday.strftime("%Y-%m-%d")
