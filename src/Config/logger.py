import logging
import os
from pathlib import Path

_fmt = "%(asctime)s  %(levelname)-8s  %(name)s  %(message)s"
_level = logging.DEBUG if os.getenv("DEBUG_MODE") == "1" else logging.INFO

logging.basicConfig(level=_level, format=_fmt, datefmt="%H:%M:%S")

# Also write to logs/aria.log
_log_dir = Path(__file__).resolve().parents[2] / "logs"
_log_dir.mkdir(exist_ok=True)
_fh = logging.FileHandler(_log_dir / "aria.log", encoding="utf-8")
_fh.setFormatter(logging.Formatter(_fmt, datefmt="%H:%M:%S"))
logging.getLogger().addHandler(_fh)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
