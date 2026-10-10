"""Device adapters: simulator for safe local execution and a clear extension point for real devices."""
from abc import ABC, abstractmethod


class NetworkDevice(ABC):
    @abstractmethod
    def connect(self):
        """Open a device session."""

    @abstractmethod
    def execute(self, command: str) -> str:
        """Execute a read-only command and return raw output."""

    @abstractmethod
    def disconnect(self):
        """Close a device session."""


class SimulatorDevice(NetworkDevice):
    """Local simulator. Outputs are fixture-backed, not collected from physical network devices."""

    def __init__(self, hostname: str, command_outputs: dict[str, str]):
        self.hostname = hostname
        self.command_outputs = command_outputs
        self.connected = False

    def connect(self):
        self.connected = True
        return True

    def execute(self, command: str) -> str:
        if not self.connected:
            raise RuntimeError(f"{self.hostname}: connect() must be called before execute()")
        try:
            return self.command_outputs[command]
        except KeyError as exc:
            raise ValueError(f"Unsupported simulated command: {command}") from exc

    def disconnect(self):
        self.connected = False
