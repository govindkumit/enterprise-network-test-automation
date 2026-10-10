"""Representative Cisco-like command outputs for parser and test development."""
DEFAULT_OUTPUTS = {
    "show vlan": "VLAN Name Status\n10 USERS active\n20 VOICE active",
    "show interfaces trunk": "Port Mode Encapsulation Status Allowed VLANs\nPo1 on 802.1q trunking 10,20",
    "show etherchannel summary": "Group Port-channel Protocol Ports\n1 Po1(LACP) LACP Eth1(P) Eth2(P)",
    "show ip ospf neighbor": "Neighbor ID Pri State Dead Time Address Interface\n2.2.2.2 1 FULL/DR 00:00:32 10.0.12.2 Gi0/0",
    "show ip bgp summary": "Neighbor V AS MsgRcvd MsgSent State/PfxRcd\n192.0.2.2 4 65002 100 99 3",
    "show ip route": "C 10.10.10.0/24 is directly connected\nO 10.20.20.0/24 [110/20] via 10.0.12.2\nB 172.16.0.0/16 [20/0] via 192.0.2.2",
    "show nve peers": "Peer-IP State Uptime\n192.0.2.12 Up 01:22:10",
    "show bgp l2vpn evpn summary": "Neighbor V AS State/PfxRcd\n192.0.2.12 4 65000 5",
}
