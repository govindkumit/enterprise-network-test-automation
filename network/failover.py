"""Pure decision logic for validating redundant-path failover in simulated scenarios."""
from dataclasses import dataclass


@dataclass(frozen=True)
class PathState:
    name: str
    healthy: bool
    preference: int


def select_active_path(paths: list[PathState]) -> str | None:
    """Select the healthy path with the lowest preference value; return None if none is healthy."""
    healthy = [path for path in paths if path.healthy]
    if not healthy:
        return None
    return min(healthy, key=lambda path: path.preference).name
