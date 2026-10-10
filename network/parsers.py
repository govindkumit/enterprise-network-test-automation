"""Small parsers for representative CLI output; validate format before using with vendor output."""
import re


def parse_vlan_ids(output: str) -> set[int]:
    return {int(v) for v in re.findall(r"(?m)^(\d+)\s+\S+\s+active\s*$", output)}


def parse_trunk_vlans(output: str) -> set[int]:
    match = re.search(r"(?m)^\S+\s+\S+\s+\S+\s+trunking\s+([\d, -]+)\s*$", output)
    if not match:
        return set()
    return {int(v) for v in re.findall(r"\d+", match.group(1))}


def parse_lag_members(output: str) -> dict[str, str]:
    return {port: state for port, state in re.findall(r"(Eth\d+)\((\w+)\)", output)}


def parse_ospf_states(output: str) -> list[str]:
    return re.findall(r"\b(FULL|2WAY|EXSTART|EXCHANGE|LOADING|INIT|DOWN)(?:/\w+)?\b", output)


def parse_bgp_established(output: str) -> bool:
    lines = [line for line in output.splitlines() if line.strip()]
    return len(lines) > 1 and bool(re.search(r"\s\d+\s*$", lines[-1]))


def parse_route_prefixes(output: str) -> set[str]:
    return set(re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}\b", output))


def parse_vxlan_peers(output: str) -> dict[str, str]:
    return {ip: state.lower() for ip, state in re.findall(r"(?m)^((?:\d{1,3}\.){3}\d{1,3})\s+(Up|Down)\b", output)}


def parse_evpn_prefix_count(output: str) -> int:
    lines = [line for line in output.splitlines() if line.strip()]
    if len(lines) < 2:
        return 0
    tail = lines[-1].split()[-1]
    return int(tail) if tail.isdigit() else 0
