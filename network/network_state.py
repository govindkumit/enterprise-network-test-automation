"""Read-only state access and mutation hooks used only for controlled test fault injection."""
from copy import deepcopy


class NetworkState:
    def __init__(self, topology: dict):
        self.topology = deepcopy(topology)
        self.faults = []

    def get_device(self, name: str) -> dict:
        return self.topology["devices"].get(name, {})

    def inject_fault(self, device: str, path: tuple, value):
        """Change simulated state only; never touches physical equipment."""
        target = self.get_device(device)
        for key in path[:-1]:
            target = target.setdefault(key, {})
        old = target.get(path[-1])
        target[path[-1]] = value
        self.faults.append({"device": device, "path": list(path), "old": old, "new": value})

    def restore_last_fault(self):
        if not self.faults:
            return False
        fault = self.faults.pop()
        target = self.get_device(fault["device"])
        for key in fault["path"][:-1]:
            target = target.setdefault(key, {})
        target[fault["path"][-1]] = fault["old"]
        return True
