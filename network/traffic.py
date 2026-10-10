"""Basic endpoint reachability and optional iperf3 traffic checks."""
from dataclasses import dataclass
import platform, shutil, subprocess

@dataclass(frozen=True)
class TrafficResult:
    success: bool
    command: tuple[str, ...]
    return_code: int
    stdout: str
    stderr: str

def ping_host(host: str, count=4, timeout_seconds=2) -> TrafficResult:
    """Run OS ping against a specified endpoint."""
    if not host or count < 1 or timeout_seconds < 1:
        raise ValueError("host is required; count and timeout_seconds must be positive")
    if platform.system().lower() == "windows":
        command = ["ping", "-n", str(count), "-w", str(timeout_seconds * 1000), host]
    else:
        command = ["ping", "-c", str(count), "-W", str(timeout_seconds), host]
    result = subprocess.run(command, capture_output=True, text=True, timeout=count * timeout_seconds + 5)
    return TrafficResult(result.returncode == 0, tuple(command), result.returncode, result.stdout, result.stderr)

def run_iperf3_client(server: str, duration_seconds=5, port=5201) -> TrafficResult:
    """Run iperf3 against an explicitly specified, authorized test server."""
    binary = shutil.which("iperf3")
    if not binary:
        raise RuntimeError("iperf3 executable was not found. Install iperf3 to use throughput tests.")
    if not server or duration_seconds < 1 or not 1 <= int(port) <= 65535:
        raise ValueError("server is required; duration must be positive and port must be 1..65535")
    command = [binary, "--client", server, "--time", str(int(duration_seconds)), "--port", str(int(port)), "--json"]
    result = subprocess.run(command, capture_output=True, text=True, timeout=int(duration_seconds) + 15)
    return TrafficResult(result.returncode == 0, tuple(command), result.returncode, result.stdout, result.stderr)
