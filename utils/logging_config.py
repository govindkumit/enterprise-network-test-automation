import logging
from pathlib import Path


def configure_logging():
    Path("reports").mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("reports/network-tests.log", encoding="utf-8"),
        ],
        force=True,
    )
