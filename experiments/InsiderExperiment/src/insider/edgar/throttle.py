"""The SEC request throttle. The only enforcement site for the registered rate.

The SEC states a ceiling of ten requests per second and returns 403 above it.
The registered rate sits below that ceiling and this module is the single place
that reads it. Delete the read and tests/test_guards.py reports
`sec_requests_per_second` as a config field enforced nowhere, which is the
failure shape the six unenforced Level 1 keys had.
"""

from __future__ import annotations

import threading
import time

from insider.config import CONFIG, Config


class Throttle:
    """A minimum-interval gate shared by every SEC request in the process."""

    def __init__(self, cfg: Config = CONFIG) -> None:
        rate = cfg.sec_requests_per_second
        if rate <= 0:
            raise ValueError("the registered request rate must be positive")
        self._min_interval = 1.0 / rate
        self._lock = threading.Lock()
        self._last_release = 0.0

    @property
    def min_interval_seconds(self) -> float:
        return self._min_interval

    def wait(self) -> float:
        """Block until the next request may go out. Returns the seconds waited."""
        with self._lock:
            now = time.monotonic()
            earliest = self._last_release + self._min_interval
            waited = 0.0
            if now < earliest:
                waited = earliest - now
                time.sleep(waited)
            self._last_release = time.monotonic()
            return waited


THROTTLE = Throttle()
