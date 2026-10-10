# Enterprise Switching & Routing Validation and Network Test Automation Framework

A portfolio-ready Python/Pytest framework demonstrating automated validation patterns for enterprise Layer 2 switching, Layer 3 routing, and VXLAN/EVPN overlay networks. Includes simulated device state, reusable validators, representative CLI output parsers, negative/fault-recovery scenarios, logs, HTML reporting, Docker, and GitHub Actions.

> **Scope and honesty:** This repository runs against a local, fixture-backed simulator. The Cisco-like command outputs are representative sample data, not collected from physical switches/routers. It does not configure or validate real hardware. The adapter interface is an extension point for a properly authorized lab using vendor-supported APIs/SSH and real device parsers.

## Capabilities

- **L2:** VLAN presence, trunk allowed VLANs, LAG state/member checks.
- **L3:** OSPF neighbor state, BGP peering state, route presence.
- **Overlay:** VXLAN peer state and EVPN route-count checks.
- **Test design:** positive, negative, fault detection, and recovery tests.
- **Engineering:** device adapter abstraction, topology-as-data (YAML), parser unit tests, structured logging.
- **Delivery:** Pytest HTML/JUnit reports, Docker, GitHub Actions artifacts.

## Architecture

```text
Topology YAML / Simulated CLI Fixtures
                 |
                 v
        Device Adapter Layer
      (Simulator; real adapter later)
                 |
                 v
       State + Output Parsers
                 |
                 v
        Reusable Validators
                 |
                 v
   Pytest: L2 | L3 | Overlay | Recovery
                 |
                 v
       Logs + HTML/JUnit Reports
                 |
                 v
       GitHub Actions / Docker
```

## Requirements

- Python 3.10+ (CI uses Python 3.12)
- Git
- Optional: Docker Desktop

## Run on Windows (PowerShell)

```powershell
git clone https://github.com/YOUR-USERNAME/enterprise-network-test-automation.git
cd enterprise-network-test-automation
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts/run_tests.py
```

If PowerShell blocks activation, use `\.venv\Scripts\python.exe -m pip install -r requirements.txt` and `\.venv\Scripts\python.exe scripts/run_tests.py`.

## Run on macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts/run_tests.py
```

## Reports

After a local run:
- `reports/pytest-report.html` — self-contained HTML report.
- `reports/network-tests.log` — execution log.

CI uploads `reports/` as a downloadable workflow artifact. The HTML report is not automatically published as a public website.

## Run selected suites

```bash
python -m pytest -m l2 -v
python -m pytest -m l3 -v
python -m pytest -m overlay -v
python -m pytest -m negative -v
python -m pytest -m recovery -v
```

## Docker

```bash
docker build -t enterprise-network-qa .
docker run --rm -v "${PWD}/reports:/app/reports" enterprise-network-qa
```

PowerShell users can use:

```powershell
docker run --rm -v "${PWD}/reports:/app/reports" enterprise-network-qa
```

## How fault injection works

The tests alter in-memory simulated state to emulate a protocol failure, assert the validator detects it, restore the prior value, and assert recovery. No packets are sent and no real device configuration is changed.

## Extending to real devices

1. Implement `NetworkDevice` for your approved lab access method.
2. Use secure secret management (environment variables or CI secrets; never commit credentials).
3. Add vendor/version-specific parsers and fixture-based parser tests.
4. Define lab topology and expected states.
5. Add guarded integration tests that are opt-in and run only against explicitly configured lab devices.
6. Validate changes first in a lab and use read-only commands by default.

Potential extensions include Cisco pyATS/Genie, Netmiko, RESTCONF/NETCONF, Robot Framework, traffic generation, convergence timing, packet loss/latency thresholds, IPv6, STP, and parallel test execution. Those integrations are not included/enabled by default.

## Framework Demonstration

1. Run all tests and open `reports/pytest-report.html`.
2. Show VLAN/LAG, OSPF/BGP, and VXLAN/EVPN suites.
3. Show the negative OSPF test detecting a simulated neighbor failure.
4. Show recovery after restoring simulated state.
5. Show the GitHub Actions run and download the report artifact.

## Project Overview

**Enterprise Switching & Routing Validation Automation Framework** — Built a Python/Pytest portfolio framework to demonstrate automated L2/L3 and VXLAN/EVPN validation, including VLAN/trunk/LAG checks, OSPF/BGP state checks, route validation, negative/fault-recovery scenarios, reusable parsers and validators, HTML reporting, Docker, and GitHub Actions CI.

Use “portfolio framework / simulated validation” unless and until you integrate and test against real network devices.

## License

Add a license if you want others to reuse the project; choose one based on your intended sharing terms.


## Real-device smoke test (opt-in)

The Netmiko adapter can run a read-only `show version` check against one lab device. Use a device you are authorized to access. Do not commit credentials to YAML, source code, GitHub, or logs.

PowerShell (replace example values with your approved lab details):

```powershell
$env:NETWORK_LAB_HOST="192.0.2.10"
$env:NETWORK_LAB_USERNAME="lab-user"
$env:NETWORK_LAB_PASSWORD="use-a-lab-secret"
$env:NETWORK_LAB_DEVICE_TYPE="cisco_ios"
$env:NETWORK_LAB_PORT="22"
python -m pytest tests/integration/test_real_device.py -v
```

Linux/macOS:

```bash
export NETWORK_LAB_HOST="192.0.2.10"
export NETWORK_LAB_USERNAME="lab-user"
export NETWORK_LAB_PASSWORD="use-a-lab-secret"
export NETWORK_LAB_DEVICE_TYPE="cisco_ios"
export NETWORK_LAB_PORT="22"
python -m pytest tests/integration/test_real_device.py -v
```

If the required environment variables are absent, the integration test is skipped. The adapter permits only commands listed in `network/netmiko_device.py` and reviewed as read-only.

## Convergence timing

`network/convergence.py` exposes `wait_for_convergence(check, timeout_seconds, poll_interval_seconds)`. Pass a read-only state check (such as whether an OSPF neighbor is `FULL`) to measure elapsed time until the condition becomes true. Current tests validate the polling utility; a meaningful protocol convergence measurement requires a reachable lab device and a defined event/observation procedure.

## Endpoint traffic checks

`network/traffic.py` provides `ping_host(host, count=4)` for IP reachability and `run_iperf3_client(server, duration_seconds=5)` for optional throughput testing when `iperf3` is installed and a test server is running. Run traffic tests only against systems and networks you are authorized to test. Ping reachability is not a substitute for application-level or performance acceptance criteria.

## Integration boundaries

- Real-device access is read-only; automated configuration changes and physical failover are not enabled. The failover selection tests exercise simulated path state, not a live routing event.
- Convergence timing measures a supplied condition; it does not itself trigger a routing event.
- Traffic tests require a reachable endpoint; iperf3 requires a separately running server.
- Device output formats vary by platform and software release. Validate parsers against sanitized output from the target lab platform before operational use.
