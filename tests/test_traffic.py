import subprocess
import pytest
from network import traffic

def test_ping_builds_platform_command_and_reports_success(monkeypatch):
    monkeypatch.setattr(traffic.platform, "system", lambda: "Linux")
    monkeypatch.setattr(traffic.subprocess, "run", lambda *a, **k: subprocess.CompletedProcess(a[0], 0, "4 packets transmitted", ""))
    result = traffic.ping_host("192.0.2.10", count=2)
    assert result.success and result.command[:3] == ("ping", "-c", "2")

def test_ping_reports_failure(monkeypatch):
    monkeypatch.setattr(traffic.platform, "system", lambda: "Linux")
    monkeypatch.setattr(traffic.subprocess, "run", lambda *a, **k: subprocess.CompletedProcess(a[0], 1, "", "unreachable"))
    result = traffic.ping_host("192.0.2.10")
    assert not result.success and result.return_code == 1

def test_ping_rejects_invalid_count():
    with pytest.raises(ValueError):
        traffic.ping_host("192.0.2.10", count=0)

def test_iperf3_requires_binary(monkeypatch):
    monkeypatch.setattr(traffic.shutil, "which", lambda _: None)
    with pytest.raises(RuntimeError, match="iperf3"):
        traffic.run_iperf3_client("192.0.2.20")
