from network.convergence import wait_for_convergence

def test_convergence_succeeds_when_condition_is_true():
    result = wait_for_convergence(lambda: True, timeout_seconds=0, poll_interval_seconds=0.01)
    assert result.converged and result.attempts == 1 and result.elapsed_seconds >= 0

def test_convergence_times_out_for_false_condition():
    result = wait_for_convergence(lambda: False, timeout_seconds=0.02, poll_interval_seconds=0.005)
    assert not result.converged and result.attempts >= 1 and result.elapsed_seconds >= 0.02

def test_convergence_rejects_invalid_poll_interval():
    import pytest
    with pytest.raises(ValueError):
        wait_for_convergence(lambda: True, poll_interval_seconds=0)
