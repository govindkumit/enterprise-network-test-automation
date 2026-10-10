"""Opt-in, read-only smoke test for an explicitly configured lab device."""
import os
import pytest
pytestmark = pytest.mark.real_device

def test_real_device_can_execute_show_version():
    required = ("NETWORK_LAB_HOST", "NETWORK_LAB_USERNAME", "NETWORK_LAB_PASSWORD")
    if not all(os.getenv(name) for name in required):
        pytest.skip("Set NETWORK_LAB_HOST, NETWORK_LAB_USERNAME and NETWORK_LAB_PASSWORD to enable lab test")
    from network.netmiko_device import NetmikoDevice
    device = NetmikoDevice.from_environment()
    try:
        assert device.connect()
        output = device.execute("show version")
        assert output and output.strip()
    finally:
        device.disconnect()
