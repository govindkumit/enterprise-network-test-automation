"""Measure how long a condition takes to become true using monotonic time."""
from dataclasses import dataclass
import time
from typing import Callable

@dataclass(frozen=True)
class ConvergenceResult:
    converged: bool
    elapsed_seconds: float
    attempts: int

def wait_for_convergence(check: Callable[[], bool], timeout_seconds=30.0, poll_interval_seconds=1.0) -> ConvergenceResult:
    """Poll a read-only condition until true or timeout; does not change device state."""
    if timeout_seconds < 0:
        raise ValueError("timeout_seconds must be >= 0")
    if poll_interval_seconds <= 0:
        raise ValueError("poll_interval_seconds must be > 0")
    started = time.monotonic()
    attempts = 0
    while True:
        attempts += 1
        if check():
            return ConvergenceResult(True, time.monotonic() - started, attempts)
        elapsed = time.monotonic() - started
        if elapsed >= timeout_seconds:
            return ConvergenceResult(False, elapsed, attempts)
        time.sleep(min(poll_interval_seconds, max(0, timeout_seconds - elapsed)))
