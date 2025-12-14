import logging
import sys
from pathlib import Path
from datetime import datetime


def get_log_file() -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base = Path(__file__).resolve().parent / "logging"
    base.mkdir(parents=True, exist_ok=True)
    return base / f"scraper_{timestamp}.log"


def setup_logging() -> None:
    log_file = get_log_file()

    formatter = logging.Formatter(
        "%(asctime)s — %(levelname)s — %(name)s — %(message)s"
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if setup_logging() is called twice
    if root_logger.handlers:
        return

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)