"""
logger.py – Structured logging setup for the project.

Every pipeline run records structured events including
timestamps, source, duration, errors, and data quality info.
"""
from __future__ import annotations

import json
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

_LOG_FILE = LOG_DIR / f"pipeline_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.jsonl"


class StructuredLogger:
    """Writes machine-readable JSONL log lines alongside human-readable console output."""

    def __init__(self, name: str, log_file: Path | None = None):
        self.name = name
        self.log_file = log_file or _LOG_FILE
        self._console = logging.getLogger(name)
        if not self._console.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s"))
            self._console.addHandler(handler)
            self._console.setLevel(logging.INFO)

    def _write(self, level: str, message: str, extra: dict[str, Any] | None = None) -> None:
        record: dict[str, Any] = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "logger": self.name,
            "level": level,
            "message": message,
        }
        if extra:
            record.update(extra)
        with self.log_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    def info(self, message: str, **kwargs: Any) -> None:
        self._console.info(message)
        self._write("INFO", message, kwargs or None)

    def warning(self, message: str, **kwargs: Any) -> None:
        self._console.warning(message)
        self._write("WARNING", message, kwargs or None)

    def error(self, message: str, **kwargs: Any) -> None:
        self._console.error(message)
        self._write("ERROR", message, kwargs or None)

    def debug(self, message: str, **kwargs: Any) -> None:
        self._console.debug(message)
        self._write("DEBUG", message, kwargs or None)


class Timer:
    """Context manager for timing pipeline stages."""

    def __init__(self, logger: StructuredLogger, stage: str):
        self.logger = logger
        self.stage = stage
        self._start: float = 0.0

    def __enter__(self) -> "Timer":
        self._start = time.perf_counter()
        self.logger.info(f"[START] {self.stage}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.perf_counter() - self._start
        if exc_type is None:
            self.logger.info(f"[DONE] {self.stage}", duration_sec=round(elapsed, 3))
        else:
            self.logger.error(f"[FAILED] {self.stage}: {exc_val}", duration_sec=round(elapsed, 3))
        return False


def get_logger(name: str) -> StructuredLogger:
    return StructuredLogger(name)
