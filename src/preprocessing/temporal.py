"""
temporal.py – Temporal alignment and sequence construction.

Handles the critical task of aligning multi-source observations
to a common timeline, preventing future data leakage, and
constructing temporal input sequences for each T0.

⚠ DATA LEAKAGE GUARD:
    For a given T0, ONLY data at or before T0 may be used
    as input features. Future data is used ONLY as target labels.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import numpy as np
import pandas as pd

from src.logger import get_logger

log = get_logger("temporal")

# Default tolerances per data source (minutes)
DEFAULT_TOLERANCE: dict[str, int] = {
    "radar": 10,
    "satellite": 20,
    "lightning": 5,
    "nwp": 60,
}


def build_timeline(
    start: datetime,
    end: datetime,
    interval_minutes: int = 15,
) -> list[datetime]:
    """
    Build a list of evenly spaced T0 timestamps between start and end.

    Args:
        start: Start datetime (timezone-aware recommended).
        end: End datetime.
        interval_minutes: Spacing between T0 timestamps.

    Returns:
        List of datetime objects.
    """
    ts = []
    current = start
    while current <= end:
        ts.append(current)
        current += timedelta(minutes=interval_minutes)
    return ts


def find_nearest_observation(
    target_time: datetime,
    available_times: list[datetime],
    tolerance_minutes: int,
    allow_future: bool = False,
) -> datetime | None:
    """
    Find the nearest observation timestamp to target_time within tolerance.

    ⚠ DATA LEAKAGE PREVENTION:
        If allow_future=False (default), only observations at or before
        target_time are considered. This is the correct mode for input
        feature construction.

    Args:
        target_time: The desired time T0.
        available_times: List of available observation times.
        tolerance_minutes: Maximum allowed time difference (minutes).
        allow_future: If True, future observations are also considered.
                      ONLY use True when constructing TARGET LABELS.

    Returns:
        Nearest valid timestamp, or None if none found within tolerance.
    """
    if not available_times:
        return None

    times_arr = np.array([t.timestamp() for t in available_times])
    target_ts = target_time.timestamp()
    tol_sec = tolerance_minutes * 60

    diffs = times_arr - target_ts

    if not allow_future:
        # ⚠ LEAKAGE GUARD: only past or present observations
        diffs = np.where(diffs > 0, np.inf, np.abs(diffs))
    else:
        diffs = np.abs(diffs)

    if np.all(np.isinf(diffs)) or np.all(np.isnan(diffs)):
        return None

    min_idx = int(np.argmin(diffs))
    if diffs[min_idx] > tol_sec:
        return None

    return available_times[min_idx]


def build_input_sequence(
    t0: datetime,
    lookback_minutes: int,
    step_minutes: int,
) -> list[datetime]:
    """
    Build the ordered sequence of past timestamps for the input window.

    All timestamps are ≤ T0 (no future leakage).

    Args:
        t0: Current analysis time.
        lookback_minutes: Total lookback window (e.g. 60 minutes).
        step_minutes: Step between sequence timesteps (e.g. 15 minutes).

    Returns:
        List of datetime objects in ascending order (oldest first).
        The last element is always T0.

    Example:
        T0=15:00, lookback=60, step=15 →
        [14:00, 14:15, 14:30, 14:45, 15:00]
    """
    assert step_minutes > 0
    steps = []
    t = t0 - timedelta(minutes=lookback_minutes)
    while t <= t0:
        steps.append(t)
        t += timedelta(minutes=step_minutes)
    # Ensure T0 is included
    if steps[-1] != t0:
        steps.append(t0)
    return steps


def build_target_times(
    t0: datetime,
    horizons_minutes: list[int],
) -> dict[int, datetime]:
    """
    Build target (label) timestamps for each forecast horizon.

    These are future timestamps and MUST NOT be used as input features.

    Args:
        t0: Current analysis time.
        horizons_minutes: List of forecast horizons in minutes.

    Returns:
        Dict mapping horizon_minutes → target datetime.
    """
    return {h: t0 + timedelta(minutes=h) for h in horizons_minutes}


def check_no_leakage(
    t0: datetime,
    feature_timestamps: list[datetime],
) -> bool:
    """
    Validate that no feature timestamp is after T0.

    This is the CRITICAL data-leakage check.
    Call this before building any training sample.

    Args:
        t0: Analysis time.
        feature_timestamps: All timestamps used in input features.

    Returns:
        True if no leakage detected.

    Raises:
        ValueError: If any feature_timestamp > t0 (data leakage detected).
    """
    for ts in feature_timestamps:
        if ts > t0:
            raise ValueError(
                f"DATA LEAKAGE DETECTED: feature timestamp {ts.isoformat()} "
                f"is after T0 {t0.isoformat()}. "
                f"Future data must not be used as input features."
            )
    return True


class TemporalAligner:
    """
    Aligns multiple data source observations to a common T0 timeline.

    Each data source can have a different update frequency and
    temporal tolerance.
    """

    def __init__(
        self,
        t0: datetime,
        lookback_minutes: int = 60,
        step_minutes: int = 15,
        tolerances: dict[str, int] | None = None,
    ):
        self.t0 = t0
        self.lookback_minutes = lookback_minutes
        self.step_minutes = step_minutes
        self.tolerances = tolerances or DEFAULT_TOLERANCE
        self.input_sequence = build_input_sequence(t0, lookback_minutes, step_minutes)

    def align_source(
        self,
        source_name: str,
        available_times: list[datetime],
    ) -> dict[datetime, datetime | None]:
        """
        For each timestamp in the input sequence, find the nearest
        available observation from this source.

        ⚠ No future observations are used.

        Returns:
            Dict mapping sequence_time → matched_observation_time (or None).
        """
        tol = self.tolerances.get(source_name, 30)
        result: dict[datetime, datetime | None] = {}
        for seq_t in self.input_sequence:
            matched = find_nearest_observation(
                target_time=seq_t,
                available_times=available_times,
                tolerance_minutes=tol,
                allow_future=False,  # ⚠ LEAKAGE GUARD
            )
            result[seq_t] = matched
        return result

    def coverage_fraction(
        self, alignment: dict[datetime, datetime | None]
    ) -> float:
        """What fraction of sequence steps have a matched observation?"""
        matched = sum(1 for v in alignment.values() if v is not None)
        return matched / len(alignment) if alignment else 0.0

    def summary(self) -> dict[str, Any]:
        return {
            "t0": self.t0.isoformat(),
            "input_sequence": [t.isoformat() for t in self.input_sequence],
            "lookback_minutes": self.lookback_minutes,
            "step_minutes": self.step_minutes,
        }
