"""Opt-in, read-only Netmiko adapter for an authorized network lab."""
import os
from network.device import NetworkDevice

ALLOWED_COMMANDS = {
    "show vlan", "show interfaces trunk", "show etherchannel summary",
    "show ip ospf neighbor", "show ip bgp summary", "show ip route",
    "show nve peers", "show bgp l2vpn evpn summary", "show version",
    "show interfaces status",
}

class NetmikoDevice(NetworkDevice):
    """Read-only CLI adapter. Credentials should come from environment variables."""
    def __init__(self, host, username, password, device_type="cisco_ios", port=22, secret=None, conn_timeout=10):
        self.host, self.username, self.password = host, username, password
        self.device_type, self.port = device_type, int(port)
        self.secret, self.conn_timeout = secret, int(conn_timeout)
        self.connection = None

    @classmethod
    def from_environment(cls):
        required = ("NETWORK_LAB_HOST", "NETWORK_LAB_USERNAME", "NETWORK_LAB_PASSWORD")
        missing = [key for key in required if not os.getenv(key)]
        if missing:
            raise RuntimeError("Missing required environment variables: " + ", ".join(missing))
        return cls(os.environ["NETWORK_LAB_HOST"], os.environ["NETWORK_LAB_USERNAME"],
                   os.environ["NETWORK_LAB_PASSWORD"], os.getenv("NETWORK_LAB_DEVICE_TYPE", "cisco_ios"),
                   os.getenv("NETWORK_LAB_PORT", "22"), os.getenv("NETWORK_LAB_SECRET") or None,
                   os.getenv("NETWORK_LAB_CONN_TIMEOUT", "10"))

    def connect(self):
        try:
            from netmiko import ConnectHandler
        except ImportError as exc:
            raise RuntimeError("Netmiko is not installed. Run: pip install -r requirements.txt") from exc
        params = {"device_type": self.device_type, "host": self.host, "username": self.username,
                  "password": self.password, "port": self.port, "conn_timeout": self.conn_timeout,
                  "fast_cli": False}
        if self.secret:
            params["secret"] = self.secret
        self.connection = ConnectHandler(**params)
        if self.secret:
            self.connection.enable()
        return True

    def execute(self, command: str) -> str:
        normalized = " ".join(command.strip().split())
        if normalized not in ALLOWED_COMMANDS:
            raise ValueError(f"Command is not in the read-only allowlist: {normalized!r}")
        if self.connection is None:
            raise RuntimeError("connect() must be called before execute()")
        return self.connection.send_command(normalized, read_timeout=30)

    def disconnect(self):
        if self.connection is not None:
            self.connection.disconnect()
            self.connection = None
