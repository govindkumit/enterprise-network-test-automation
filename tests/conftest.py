from pathlib import Path
import yaml
import pytest

from network.network_state import NetworkState
from utils.logging_config import configure_logging


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    configure_logging()


@pytest.fixture
def network():
    config_path = Path(__file__).parents[1] / "config" / "topology.yaml"
    with config_path.open(encoding="utf-8") as handle:
        topology = yaml.safe_load(handle)
    return NetworkState(topology)
