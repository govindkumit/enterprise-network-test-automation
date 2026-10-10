from network.command_fixtures import DEFAULT_OUTPUTS
from network.device import SimulatorDevice
from network.parsers import (
    parse_vlan_ids, parse_trunk_vlans, parse_lag_members, parse_ospf_states,
    parse_bgp_established, parse_route_prefixes, parse_vxlan_peers,
    parse_evpn_prefix_count,
)


def test_simulator_device_connection_lifecycle():
    device = SimulatorDevice("LEAF-01", DEFAULT_OUTPUTS)
    device.connect()
    assert "10 USERS active" in device.execute("show vlan")
    device.disconnect()


def test_parse_vlan_and_trunk_output():
    assert parse_vlan_ids(DEFAULT_OUTPUTS["show vlan"]) == {10, 20}
    assert parse_trunk_vlans(DEFAULT_OUTPUTS["show interfaces trunk"]) == {10, 20}


def test_parse_lag_output():
    assert parse_lag_members(DEFAULT_OUTPUTS["show etherchannel summary"]) == {"Eth1": "P", "Eth2": "P"}


def test_parse_ospf_output():
    assert "FULL" in parse_ospf_states(DEFAULT_OUTPUTS["show ip ospf neighbor"])


def test_parse_bgp_output():
    assert parse_bgp_established(DEFAULT_OUTPUTS["show ip bgp summary"])


def test_parse_routes_output():
    assert {"10.10.10.0/24", "10.20.20.0/24", "172.16.0.0/16"} <= parse_route_prefixes(DEFAULT_OUTPUTS["show ip route"])


def test_parse_vxlan_and_evpn_output():
    assert parse_vxlan_peers(DEFAULT_OUTPUTS["show nve peers"])["192.0.2.12"] == "up"
    assert parse_evpn_prefix_count(DEFAULT_OUTPUTS["show bgp l2vpn evpn summary"]) == 5


def test_netmiko_adapter_rejects_configuration_commands():
    from network.netmiko_device import NetmikoDevice
    device = NetmikoDevice("example.invalid", "user", "password")
    import pytest
    with pytest.raises(ValueError, match="read-only allowlist"):
        device.execute("configure terminal")
