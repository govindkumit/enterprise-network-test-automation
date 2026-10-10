"""Reusable assertions against the simulated desired/observed state."""
class NetworkValidator:
    @staticmethod
    def vlan_present(state, device, vlan):
        return vlan in state.get_device(device).get("vlans", [])

    @staticmethod
    def trunk_allows_vlan(state, device, vlan):
        return vlan in state.get_device(device).get("trunk_allowed_vlans", [])

    @staticmethod
    def lag_up(state, device):
        return state.get_device(device).get("lag", {}).get("status") == "up"

    @staticmethod
    def lag_members_healthy(state, device):
        lag = state.get_device(device).get("lag", {})
        return bool(lag.get("members")) and lag.get("status") == "up"

    @staticmethod
    def ospf_full(state, device):
        ospf = state.get_device(device).get("ospf", {})
        return ospf.get("enabled") is True and bool(ospf.get("neighbors")) and all(
            n.get("state") == "FULL" for n in ospf["neighbors"]
        )

    @staticmethod
    def bgp_established(state, device):
        bgp = state.get_device(device).get("bgp", {})
        return bgp.get("enabled") is True and bool(bgp.get("neighbors")) and all(
            n.get("state") == "ESTABLISHED" for n in bgp["neighbors"]
        )

    @staticmethod
    def route_present(state, device, prefix):
        return prefix in state.get_device(device).get("routes", [])

    @staticmethod
    def vxlan_peer_up(state, device):
        vxlan = state.get_device(device).get("vxlan", {})
        return vxlan.get("enabled") is True and vxlan.get("peer_state") == "up"

    @staticmethod
    def evpn_has_routes(state, device, minimum=1):
        evpn = state.get_device(device).get("evpn", {})
        return evpn.get("enabled") is True and evpn.get("routes", 0) >= minimum
