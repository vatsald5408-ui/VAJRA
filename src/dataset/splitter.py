"""
splitter.py – Temporal train/val/test split.

⚠ NEVER randomly split individual rows — weather samples
  from the same storm are highly correlated.

Uses time-based splitting with a configurable gap to prevent
any storm event near the boundary from appearing in multiple splits.
"""
from __future__ import annotations

from datetime import datetime, timedelta

import pandas as pd

from src.logger import get_logger

log = get_logger("dataset.splitter")


def temporal_split(
    df: pd.DataFrame,
    train_end: str,
    val_end: str,
    gap_days: int = 30,
    timestamp_col: str = "timestamp",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Split DataFrame into train / validation / test by timestamp.

    A temporal gap of `gap_days` is enforced between splits to
    ensure storm events near boundaries do not bleed across splits.

    Args:
        df: Full dataset DataFrame.
        train_end: Last date included in training (ISO string).
        val_end: Last date included in validation (ISO string).
        gap_days: Days of gap to exclude between splits.
        timestamp_col: Name of timestamp column.

    Returns:
        (train_df, val_df, test_df)
    """
    df = df.copy()
    df["_ts"] = pd.to_datetime(df[timestamp_col])

    te = pd.Timestamp(train_end)
    ve = pd.Timestamp(val_end)

    train_mask = df["_ts"] <= te
    val_start = te + timedelta(days=gap_days)
    val_mask = (df["_ts"] > val_start) & (df["_ts"] <= ve)
    test_start = ve + timedelta(days=gap_days)
    test_mask = df["_ts"] > test_start

    train_df = df[train_mask].drop(columns=["_ts"]).copy()
    val_df = df[val_mask].drop(columns=["_ts"]).copy()
    test_df = df[test_mask].drop(columns=["_ts"]).copy()

    log.info(
        "Temporal split complete",
        train_samples=len(train_df),
        val_samples=len(val_df),
        test_samples=len(test_df),
        gap_days=gap_days,
    )

    if len(test_df) == 0:
        log.warning(
            "Test set is EMPTY. This is expected in DEMO mode with short date ranges. "
            "In production, ensure test period dates are configured correctly."
        )

    return train_df, val_df, test_df
