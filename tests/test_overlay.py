import pytest
from network.validators import NetworkValidator as V


@pytest.mark.overlay
@pytest.mark.parametrize("device", ["leaf1", "leaf2"])
def test_vxlan_peer_is_up(network, device):
    assert V.vxlan_peer_up(network, device)


@pytest.mark.overlay
@pytest.mark.parametrize("device", ["leaf1", "leaf2"])
def test_evpn_has_expected_routes(network, device):
    assert V.evpn_has_routes(network, device, minimum=5)
