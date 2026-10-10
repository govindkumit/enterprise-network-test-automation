import pytest
from network.validators import NetworkValidator as V


@pytest.mark.negative
def test_detects_ospf_neighbor_failure(network):
    network.inject_fault("router1", ("ospf", "neighbors"), [{"address": "10.0.12.2", "state": "DOWN"}])
    assert not V.ospf_full(network, "router1")


@pytest.mark.recovery
def test_state_recovers_after_fault_is_restored(network):
    assert V.bgp_established(network, "router1")
    network.inject_fault("router1", ("bgp", "neighbors"), [{"address": "192.0.2.2", "state": "IDLE"}])
    assert not V.bgp_established(network, "router1")
    assert network.restore_last_fault()
    assert V.bgp_established(network, "router1")
