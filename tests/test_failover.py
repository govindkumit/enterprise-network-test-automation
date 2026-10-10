import pytest
from network.failover import PathState, select_active_path


@pytest.mark.recovery
def test_traffic_uses_primary_path_when_both_paths_are_healthy():
    paths = [PathState("primary", True, 10), PathState("backup", True, 20)]
    assert select_active_path(paths) == "primary"


@pytest.mark.recovery
def test_backup_path_is_selected_when_primary_fails():
    paths = [PathState("primary", False, 10), PathState("backup", True, 20)]
    assert select_active_path(paths) == "backup"


@pytest.mark.negative
def test_no_path_is_selected_when_all_paths_fail():
    paths = [PathState("primary", False, 10), PathState("backup", False, 20)]
    assert select_active_path(paths) is None


def test_empty_path_list_has_no_active_path():
    assert select_active_path([]) is None
