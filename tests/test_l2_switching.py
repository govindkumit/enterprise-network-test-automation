import pytest
from network.validators import NetworkValidator as V


@pytest.mark.l2
@pytest.mark.parametrize("device,vlan", [("leaf1", 10), ("leaf1", 20), ("leaf2", 10), ("leaf2", 20)])
def test_expected_vlans_exist(network, device, vlan):
    assert V.vlan_present(network, device, vlan)


@pytest.mark.l2
@pytest.mark.parametrize("device,vlan", [("leaf1", 10), ("leaf1", 20), ("leaf2", 10), ("leaf2", 20)])
def test_trunk_allows_expected_vlans(network, device, vlan):
    assert V.trunk_allows_vlan(network, device, vlan)


@pytest.mark.l2
@pytest.mark.parametrize("device", ["leaf1", "leaf2"])
def test_lag_is_up_with_members(network, device):
    assert V.lag_up(network, device)
    assert V.lag_members_healthy(network, device)


@pytest.mark.negative
def test_unconfigured_vlan_is_not_present(network):
    assert not V.vlan_present(network, "leaf1", 999)
