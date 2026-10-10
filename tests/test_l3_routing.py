import pytest
from network.validators import NetworkValidator as V


@pytest.mark.l3
@pytest.mark.parametrize("device", ["router1", "router2"])
def test_ospf_neighbors_are_full(network, device):
    assert V.ospf_full(network, device)


@pytest.mark.l3
@pytest.mark.parametrize("device", ["router1", "router2"])
def test_bgp_peers_are_established(network, device):
    assert V.bgp_established(network, device)


@pytest.mark.l3
def test_expected_route_is_present(network):
    assert V.route_present(network, "router1", "10.20.20.0/24")


@pytest.mark.negative
def test_unexpected_route_is_not_present(network):
    assert not V.route_present(network, "router1", "203.0.113.0/24")
